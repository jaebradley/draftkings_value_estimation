import urllib2 as url
from pandas import DataFrame
from StringIO import StringIO
import csv

def return_draftkings_daily_nba_player_salary_as_dataframe(today):
    draftkings_nba_player_salary_url = 'https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=5&draftGroupId=5964'
    response = url.urlopen(draftkings_nba_player_salary_url).read().replace('"','').split('\r\n')
    response = response[1:len(response) - 1]
    draftkings_player_list = list()
    for player in response:
        player = player.replace("'",'').split(',')
        player.append(today)
        draftkings_player_list.append(player)
    draftkings_player_dataframe = DataFrame(draftkings_player_list,columns=['position','name','salary','date'])
    return draftkings_player_dataframe
