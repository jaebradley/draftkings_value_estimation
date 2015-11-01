from basketball_reference_web_scraper.models.schedule import Schedule
from basketball_reference_web_scraper.models.event import Event
import json


def return_event_from_json_encoded_event(json_encoded_event):
    json_encoded_event_dictionary = json.loads(json_encoded_event)
    return Event(
        json_encoded_event_dictionary['start_time'],
        json_encoded_event_dictionary['visiting_team_name'],
        json_encoded_event_dictionary['home_team_name']
    )


def return_schedule_from_json_encoded_schedule(json_encoded_schedule):
    schedule_dictionary = json.loads(json_encoded_schedule)
    json_encoded_parsed_event_list = schedule_dictionary['parsed_event_list']
    parsed_event_list = list()
    for json_encoded_parsed_event in json_encoded_parsed_event_list:
        parsed_event_list.append(return_event_from_json_encoded_event(json_encoded_event=json_encoded_parsed_event))
    return Schedule(
        parsed_event_list=parsed_event_list,
        end_year=schedule_dictionary['end_year'],
        start_year=schedule_dictionary['start_year']
    )