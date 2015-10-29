from basketball_reference_web_scraper.readers import return_json_encoded_box_scores_for_date
from basketball_reference_web_scraper.readers import return_schedule
import pytz
import datetime


def write_box_scores_for_season_to_json(season_start_year):
    est = pytz.timezone("US/Eastern")
    season_schedule = return_schedule(season_start_year=season_start_year)
    distinct_est_dates = set([est.localize(event.start_time).date() for event in season_schedule.parsed_event_list])
    for est_date in distinct_est_dates:
        while est_date <= datetime.datetime.now(tz=est).date():
            json_encoded_box_score = return_json_encoded_box_scores_for_date(date=est_date)
            formatted_date = est_date.datetime.strftime("%Y_%m_%d")
            with open("../static/box_scores/{0}.json".format(formatted_date)) as json_file:
                json_file.write(json_encoded_box_score)
                json_file.close()