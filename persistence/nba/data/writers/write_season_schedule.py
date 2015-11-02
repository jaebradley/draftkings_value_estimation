from basketball_reference_web_scraper.readers import return_json_encoded_schedule


def write_season_schedule_to_json(season_start_year, output_file_path):
    json_encoded_schedule = return_json_encoded_schedule(season_start_year=season_start_year)
    with open(output_file_path, "w+") as json_file:
        json_file.write(json_encoded_schedule)
        json_file.close()