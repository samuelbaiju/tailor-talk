from gcal.calendar_auth import get_calendar_service
def book_time(summary, start, end):
    try:
        service = get_calendar_service()
        event = {
            'summary': summary,
            'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'},
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ Event created: {event.get('htmlLink')}"
    except Exception as e:
        return f"❌ Failed to create event: {e}"
# This function books a time slot in the user's primary Google Calendar.
# It takes a summary, start time, and end time as parameters.

from .calendar_auth import get_calendar_service
from datetime import datetime, timedelta

def is_slot_free(start_time: datetime, end_time: datetime) -> bool:
    service = get_calendar_service()
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time.isoformat() ,
        timeMax=end_time.isoformat() ,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    print(f"📅 Found {len(events)} event(s) between {start_time} and {end_time}")
    return len(events) == 0