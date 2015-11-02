# read from file
# create objects
# insert objects into db

from persistence.nba.data.file_readers.schedule import return_schedule_from_json_encoded_schedule


def insert_json_encoded_schedule_into_database(json_encoded_schedule):
    schedule = return_schedule_from_json_encoded_schedule(json_encoded_schedule=json_encoded_schedule)
