from src.web_scraping.basketball_reference.boxscores.box_score_url_generator import BoxScoreUrlGenerator
from src.web_scraping.basketball_reference.boxscores.box_scores_html_returner import BoxScoresHtmlReturner
from src.persistence.model.box_score import BoxScore

import datetime
import time

class ParsedBoxScoresReturner:

    def __init__(self):
        pass

    def return_raw_box_score_list_of_lists(self, box_scores_html):
        box_scores_list = list()
        header_count = len(box_scores_html.xpath('//tr[@class=""]/th//@data-stat'))
        player_html = box_scores_html.xpath('//tr[@class=""]/td')
        count = 0
        while count < len(player_html):
            start = count
            stop = count + header_count
            box_scores_list.append([box_score_element.text_content() for box_score_element in player_html[start:stop]])
            count = stop
        return box_scores_list

    def return_box_scores(self, box_scores_html):
        box_score_list_of_lists = self.return_raw_box_score_list_of_lists(box_scores_html)
        box_scores = list()
        for box_score_list in box_score_list_of_lists:
            full_name = box_score_list[1]
            first_name = full_name.split(",")[0]
            last_name = full_name.split(",")[1]
            x = time.strptime(box_score_list[5], "%M:%S")
            seconds_played = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            box_score = BoxScore(
                first_name,
                last_name,
                None,
                box_score_list[2],
                box_score_list[4],
                seconds_played,
                box_score_list[6],
                box_score_list[7],
                box_score_list[9],
                box_score_list[10],
                box_score_list[11],
                box_score_list[12],
                box_score_list[14],
                box_score_list[15],
                box_score_list[16],
                box_score_list[17],
                box_score_list[18],
                box_score_list[19],
                box_score_list[20],
                box_score_list[21],
                box_score_list[22]
            )
            box_scores.append(box_score)
        return box_scores


url = BoxScoreUrlGenerator.generate_url(10, 2, 2015)
html = BoxScoresHtmlReturner.return_html(url)
ParsedBoxScoresReturner.return_raw_box_score_list_of_lists(html)