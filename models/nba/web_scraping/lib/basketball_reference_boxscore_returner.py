from __future__ import division
import urllib2 as url
import lxml.html as html
from pandas import DataFrame
from decimal import *
from datetime import date


def return_box_score_url(date):
    month = date.month
    day = date.day
    year = date.year

    box_score_date_arguments = {
    'month':month,
    'day':day,
    'year':year
    }
    box_score_url = 'http://www.basketball-reference.com/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(**box_score_date_arguments)
    return box_score_url

def return_box_score_column_names(box_score_url):
    content = url.urlopen(box_score_url).read()
    box_score_html = html.fromstring(content)
    headers = box_score_html.xpath('//tr[@class=""]/th//@data-stat')
    return headers

def return_raw_box_score(box_score_url):
    content = url.urlopen(box_score_url).read()
    box_score_html = html.fromstring(content)
    player_html = box_score_html.xpath('//tr[@class=""]/td')
    raw_player_box_score_list = list()
    for player in player_html:
        data = player.text_content()
        raw_player_box_score_list.append(data)
    return raw_player_box_score_list

def return_formatted_box_score_as_dataframe(raw_box_score_list,box_score_column_names,date):
    formatted_box_score_list = list()
    step = len(box_score_column_names)
    stop = len(raw_box_score_list) - 1
    for start_position in range(0,stop, step):
        end_position = start_position + step
        player_box_score = raw_box_score_list[start_position:end_position]
        temp_dict = dict()
        for count in range(0,step):
            element = player_box_score[count]
            key = box_score_column_names[count]
            if 'mp' == key:
                element = '00:' + element
            elif 'fg_pct' == key or 'fg3_pct' == key or 'ft_pct' == key:
                element = '0' + element
            elif 'game_location' == key:
                if '@' == element:
                    element = 'AWAY'
                elif '' == element:
                    element = 'HOME'
            temp_dict[key] = element
        draftkings_score = int(temp_dict['pts']) + 0.5 * int(temp_dict['fg3']) + 1.25 * int(temp_dict['trb']) + 1.5 * int(temp_dict['ast']) + 2 * int(temp_dict['stl']) + 2 * int(temp_dict['blk']) - 0.5 * int(temp_dict['tov'])
        temp_dict['draftkings_score'] = draftkings_score
        temp_dict['date'] = date
        formatted_box_score_list.append(temp_dict)
    box_score_df = DataFrame.from_dict(formatted_box_score_list)
    return box_score_df



