from basketball_reference_web_scraper.readers import return_json_encoded_schedule


def write_season_schedule_to_json():
    for season_start_year in range(2014, 2016):
        json_encoded_schedule = return_json_encoded_schedule(season_start_year=season_start_year)
        with open("../static/schedules/{0}.json".format(season_start_year)) as json_file:
            json_file.write(json_encoded_schedule)
            json_file.close()