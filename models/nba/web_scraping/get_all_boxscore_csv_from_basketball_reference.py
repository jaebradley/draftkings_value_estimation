from models.nba.web_scraping.utils.return_boxscore_csv_from_basketball_reference import return_boxscore_csv
from models.nba.web_scraping.utils.date_utils import daterange
import datetime as dt

start_date = dt.date(year=2015, month=4, day=9)
yesterday = dt.date.today() - dt.timedelta(days=1)
end_date = dt.date.today()

for single_date in daterange(start_date,end_date):
    print single_date
    try:
        return_boxscore_csv(date=single_date)
    except Exception as error_message:
        print error_message
        pass
