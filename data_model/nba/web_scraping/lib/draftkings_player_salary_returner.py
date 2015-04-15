import urllib2 as url
from pandas import DataFrame
from StringIO import StringIO
import csv

def return_draftkings_daily_nba_player_salary_as_dataframe(date):
    draftkings_nba_player_salary_url = 'https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=5&draftGroupId=6003'
    response = url.urlopen(draftkings_nba_player_salary_url).read().replace('"','').split('\r\n')
    response = response[1:len(response) - 1]
    draftkings_player_list = list()
    for player in response:
        player = player.replace("'",'').split(',')
        position = player[0]
        first_name = player[1].split(" ")[0]
        last_name = player[1].split(" ")[1]
        salary = player[2]
        player = [position, first_name, last_name, salary, date]
        draftkings_player_list.append(player)
    draftkings_player_dataframe = DataFrame(draftkings_player_list,columns=['position','first_name','last_name','salary','date'])
    return draftkings_player_dataframe
