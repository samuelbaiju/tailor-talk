import os
from datetime import datetime, timedelta
import dateparser
import re
from dotenv import load_dotenv
from openai import OpenAI
from gcal.calendar_utils import book_time
from dateparser.search import search_dates
import parsedatetime as pdt
from gcal.calendar_utils import is_slot_free
import pytz
from gcal.calendar_auth import get_calendar_service
from datetime import time

if os.getenv("RENDER") != "true":  # or check for DEBUG=True
    load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
print("🔑 ENV OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))

def correct_common_typos(text: str) -> str:
    corrections = {
        "tommorow": "tomorrow",
        "mondayy": "monday",
        "todai": "today",
        "saterday": "saturday",
        "tmrw": "tomorrow",
        "tonite": "tonight"
        # Add more if needed
    }
    for wrong, right in corrections.items():
        text = re.sub(rf'\b{wrong}\b', right, text, flags=re.IGNORECASE)
    return text





def extract_datetime(user_input: str) -> tuple[datetime | None, str | None]:
    cal = pdt.Calendar()
    tz = pytz.timezone("Asia/Kolkata")  # You can change to your actual timezone

    # 🧼 Clean input: june30 → june 30
    user_input= correct_common_typos(user_input)
    clean_input = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', user_input)
    clean_input = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', clean_input)

    print("🧪 [CLEANED INPUT]:", clean_input)

    # Parse using parsedatetime
    now = datetime.now(tz)  # Get current time in your timezone
    time_struct, parse_status = cal.parse(clean_input, now)
    if parse_status == 0:
        print("❌ Parsing failed.")
        return None, None

    dt = datetime(*time_struct[:6])

    # ⏰ Handle time range like "between 3 and 5 pm"
    match = re.search(
        r'between (\d{1,2})\s*(am|pm)?\s*(?:-|to|and)\s*(\d{1,2})\s*(am|pm)?',
        clean_input.lower()
    )
    if match:
        h1, p1, h2, p2 = match.groups()
        h1 = int(h1)
        if p1 == 'pm' and h1 < 12:
            h1 += 12
        dt = dt.replace(hour=h1, minute=0)
        print(f"⏱️ Detected time range → booking at {h1}:00")

    # Remove seconds and microseconds
    dt = dt.replace(second=0, microsecond=0)

    # 🌐 Add timezone awareness (only if dt is naive)
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        dt = tz.localize(dt)

    # 🧠 Safety check: if date is >1 year in future, probably wrong
    now = datetime.now(tz)
    if (dt - now).days > 365:
        print("⚠️ Date parsed too far in future → suggesting rephrasing")
        return None, "next week or a closer date"

    # 🤔 Vague input like "tomorrow" without time
    if (dt.date() - now.date()).days <= 1 and dt.hour == 0:
        suggestion = now + timedelta(days=2)
        return None, suggestion.strftime("%A, %B %d")

    # ⏰ Default time fallback (if not set)
    if dt.hour == 0:
        dt = dt.replace(hour=10)

    return dt, None


async def check_availability(user_input: str) -> str:
    date, suggestion = extract_datetime(user_input)
    if not date:
        return f"⚠️ I couldn’t understand the date. {f'Did you mean {suggestion}?' if suggestion else 'Please rephrase it.'}"

    service = get_calendar_service()

    start_of_day = date.replace(hour=9, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=18, minute=0, second=0, microsecond=0)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    # Build busy slots
    busy_slots = [(datetime.fromisoformat(e['start']['dateTime']), datetime.fromisoformat(e['end']['dateTime'])) for e in events]

    # Generate free slots in 30-min blocks
    slot = start_of_day
    free_blocks = []

    while slot < end_of_day:
        next_slot = slot + timedelta(minutes=30)
        overlap = any(b[0] < next_slot and b[1] > slot for b in busy_slots)
        if not overlap:
            free_blocks.append(f"{slot.strftime('%I:%M %p')} – {next_slot.strftime('%I:%M %p')}")
        slot = next_slot

    if not free_blocks:
        return f"❌ Sorry, you’re fully booked on {date.strftime('%A, %B %d')}."
    
    return f"✅Tailor-Talk is free on **{date.strftime('%A, %B %d')}** at these times:\n\n" + "\n".join(f"• {block}" for block in free_blocks)


async def generate_response(user_input):
    try:
        user_lower = user_input.lower()

        if any(q in user_lower for q in ["free time", "any time", "available time", "availability"]):
            return await check_availability(user_input)

        # ✅ Check for booking-related keywords
        if any(keyword in user_lower for keyword in ["book", "schedule", "set up", "can you", "arrange"]):
            parsed_date, suggestion = extract_datetime(user_input)
            print("🔍 Raw user input:", user_input)
            print("🔍 Extracted datetime:", parsed_date)

            if not parsed_date:
                if suggestion:
                    return f"🤔 I wasn’t confident about the date you meant.\nDid you mean **{suggestion}**?"
                return "⚠️ Sorry, I couldn’t understand the date. Can you rephrase it?"

            # Format start and end times
            # parsed_date is already timezone-aware from extract_datetime()
            start_dt = parsed_date.replace(second=0, microsecond=0)
            end_dt = start_dt + timedelta(minutes=30)

            # ✅ Check for existing calendar conflicts
            print(f"📅 Checking slot: {start_dt} to {end_dt}")
            if not is_slot_free(start_dt, end_dt):
                return f"⚠️ Sorry, you already have a meeting scheduled on {parsed_date.strftime('%A, %B %d at %I:%M %p')}."

            # ✅ Proceed to book the event
            calendar_status = book_time("TailorTalk Meeting", start_dt.isoformat(), end_dt.isoformat())

            # Confirm using GPT
            gpt_response = client.chat.completions.create(
                model="mistralai/mixtral-8x7b-instruct",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that confirms scheduled meetings."},
                    {"role": "user", "content": f"A user scheduled a meeting on {parsed_date}. Confirm the booking clearly and politely."}
                ]
            )
            friendly = gpt_response.choices[0].message.content

            return f"""{friendly}

✅ Meeting booked!
📅 **Date & Time**: {parsed_date.strftime('%A, %B %d at %I:%M %p')}
📤 {calendar_status}
"""

        # ✅ Normal assistant response (not booking-related)
        gpt = client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=[
                {"role": "system", "content": "You are a friendly assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return gpt.choices[0].message.content

    except Exception as e:
        print("❌ Error:", e)
        return f"❌ Failed to process your request: {e}"
