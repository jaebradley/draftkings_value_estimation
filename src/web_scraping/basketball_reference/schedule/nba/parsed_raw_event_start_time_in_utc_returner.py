import time
import datetime
import pytz


class ParsedRawEventStartTimeInUtcReturner:
    def __init__(self):
        pass

    @staticmethod
    def return_parsed_start_time_in_utc(raw_event_date, raw_event_hour_of_day):
        parsed_event_date = time.strptime(raw_event_date, "%a, %b %d, %Y")
        parsed_hour_of_day = time.strptime(raw_event_hour_of_day, "%I:%M %p")
        return datetime.datetime.combine(parsed_event_date, parsed_hour_of_day)
