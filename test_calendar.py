from gcal.calendar_utils import book_time
from datetime import datetime, timedelta

# Create a test event 1 minute from now
start = (datetime.now() + timedelta(minutes=1)).isoformat()
end = (datetime.now() + timedelta(minutes=31)).isoformat()

print(book_time("Test Meeting from TailorTalk", start, end))
