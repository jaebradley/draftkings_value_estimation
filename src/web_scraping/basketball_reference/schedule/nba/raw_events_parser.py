from src.persistence.model.event import Event
import time


class RawEventsParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_raw_events(raw_events):
        event_list = list()
        for counter in range(0, raw_events.__len__(), 9):
            event_information = raw_events[counter:counter + 9]
            event = Event(
                event_information[0]
            )