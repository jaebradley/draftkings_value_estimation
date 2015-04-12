import urllib2 as url
from pandas import DataFrame
from lxml import html

def return_rotoworld_player_url_list():

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    rotoworldLineupURL = 'http://www.rotoworld.com/teams/depth-charts/nba.aspx'
    request = url.Request(rotoworldLineupURL,headers=header)
    page = url.urlopen(request).read()
    raw_lineup_html = html.fromstring(page)
    player_list = raw_lineup_html.xpath('//td/a/text()')
    link_list = raw_lineup_html.xpath('//td//a/@href')
    rotoworld_player_url_list = dict()
    for player in player_list:
        index = player_list.index(player)
        rotoworld_player_url_list[player] = 'http://www.rotoworld.com' + link_list[index]
    return rotoworld_player_url_list

def return_rotoworld_player_status():

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    rotoworld_lineup_url = 'http://www.rotoworld.com/teams/depth-charts/nba.aspx'
    request = url.Request(rotoworld_lineup_url,headers=header)
    page = url.urlopen(request).read()
    lineup_raw = html.fromstring(page)
    player_list = lineup_raw.xpath('//div[@class="playercard"]/@id')
    status_list = lineup_raw.xpath('//div[@class="playercard"]/span/text()')
    report_list = lineup_raw.xpath('//div[@class="report"]/text()')
    player_list = player_list[1:]
    status_list = status_list[1:]
    count = 0
    rotoworld_status_update_list = list()
    for player in player_list:
        temp_dict = {
            'rotoworld_player_id': player,
            'status': status_list[count],
            'report': report_list[count]
        }
        rotoworld_status_update_list.append(temp_dict)
        count += 1
    return rotoworld_status_update_list

def return_rotoworld_player_news(rotoworldPlayerURL):

    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    request = url.Request(rotoworldPlayerURL,headers=header)
    page = url.urlopen(request).read()
    player_page = html.fromstring(page)
    player_recent_performance_news_list = player_page.xpath('//div[@class="playernews"]/div[@class="report"]/text()')
    player_general_news_list = player_page.xpath('//div[@class="playernews"]/div[@class="impact"]/text()')
    player_news_date_list = player_page.xpath('//div[@class="playernews"]/div[@class="impact"]/span[@class="date"]/text()')
    news = {
        'recent_performance': player_recent_performance_news_list[0],
        'impact': player_general_news_list[0],
        'date': player_news_date_list[0]
    }
    return news

def insertAllPlayerNewsIntoMySQL(conn,rotoworldPlayerURLDict):
    for key,value in rotoworldPlayerURLDict.iteritems():
        print key
        playerNewsDict = dict()
        news = return_rotoworld_player_news(value)
        playerNewsDict[key] = news
        playerNewsDf = DataFrame(playerNewsDict.items(),columns=['name','news'])
        playerNewsDf.to_sql(name='daily_player_news',con=conn,flavor='mysql',if_exists='append',index=False)

def return_rotoworld_player_information():

    rotoworld_player_status_list = return_rotoworld_player_status()
    all_players_with_statuses = [player['rotoworld_player_id'] for player in rotoworld_player_status_list]
    rotoworld_player_url_dict = return_rotoworld_player_url_list()
    rotoworld_player_list = list()
    for key,value in rotoworld_player_url_dict.iteritems():
        rotoworld_player_name = key
        rotoworld_player_name_list = rotoworld_player_name.split(" ")
        rotoworld_player_first_name = rotoworld_player_name_list[0]
        rotoworld_player_last_name = rotoworld_player_name_list[1]
        rotoworld_player_url = value
        rotoworld_player_id = value.split("/")[5]
        if rotoworld_player_id in all_players_with_statuses:
            player_status = rotoworld_player_status_list[all_players_with_statuses.index(rotoworld_player_id)]
            temp_dict = {
                'first_name': rotoworld_player_first_name,
                'last_name': rotoworld_player_last_name,
                'rotoworld_player_id': rotoworld_player_id,
                'rotoworld_player_url': rotoworld_player_url,
                'status': player_status['status'],
                'report': player_status['report']
            }
        else:
            temp_dict = {
                'first_name': rotoworld_player_first_name,
                'last_name': rotoworld_player_last_name,
                'rotoworld_player_id': rotoworld_player_id,
                'rotoworld_player_url': rotoworld_player_url,
                'status': '',
                'report': ''
            }
        rotoworld_player_list.append(temp_dict)
    count = 0
    rotoworld_player_list = rotoworld_player_list
    for player in rotoworld_player_list:
        print "Getting Rotoworld data for {0} {1}".format(player['first_name'], player['last_name'])
        player_url = player['rotoworld_player_url']
        player_news = return_rotoworld_player_news(player_url)
        rotoworld_player_list[count]['recent_performance'] = player_news['recent_performance']
        rotoworld_player_list[count]['impact'] = player_news['impact']
        rotoworld_player_list[count]['impact_date'] = player_news['date']
        count += 1

    return rotoworld_player_list