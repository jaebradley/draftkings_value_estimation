import urllib2

from lxml import html

from src.web_scraping.basketball_reference.schedule.nba.nba_schedule_url_generator import NBAScheduleUrlGenerator


class ScheduleWebScraper:
    def __init__(self):
        pass

    def return_raw_events(self, year):
        raw_content = urllib2.urlopen(NBAScheduleUrlGenerator.generate_url(year)).read()
        schedule_html = html.fromstring(raw_content)
        events = schedule_html.xpath('//td')
        return events
