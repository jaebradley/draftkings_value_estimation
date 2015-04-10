import urllib2 as url
import lxml.html as html


def return_player_position():
    player_position_url = "http://www.basketball-reference.com/leagues/NBA_2015_totals.html"
    content = url.urlopen(player_position_url).read()
    box_score_doc = html.fromstring(content)
    player_position_raw_html_elements = box_score_doc.xpath('//tr[@class="full_table" or @class="italic_text partial_table"]/td')
    player_position_raw_list = list()
    for player in player_position_raw_html_elements:
        data = player.text_content()
        player_position_raw_list.append(data)
    return player_position_raw_list

def return_player_position_url():
    player_position_url = "http://www.basketball-reference.com/leagues/NBA_2015_totals.html"
    content = url.urlopen(player_position_url).read()
    box_score_doc = html.fromstring(content)
    player_position_raw_html_elements = box_score_doc.xpath('//tr[@class="full_table" or @class="italic_text partial_table"]/td/a')
    player_position_raw_list = list()
    for player in player_position_raw_html_elements:
        if "player" in player.attrib['href']:
            data = "http://www.basketball-reference.com" + player.attrib['href']
            player_position_raw_list.append(data)
    return player_position_raw_list

def return_player_position_list():
    raw_player_position_list = return_player_position()
    player_position_list = list()
    print raw_player_position_list[:300]
    for n in range(0, len(raw_player_position_list), 30):
        player = raw_player_position_list[n + 1]
        position = raw_player_position_list[n + 2]
        team_id = raw_player_position_list[n + 4]
        if team_id == "TOT" or "-" in position or position == "G" or position == "F":
            continue
        else:
            raw_names = player.split(" ",)
            first_name = raw_names[0]
            last_name = raw_names[1]
            if not any(d[0] == first_name and d[1] == last_name for d in player_position_list):
                temp_list = [
                    first_name,
                    last_name,
                    position,
                    team_id
                ]
                player_position_list.append(temp_list)
            else:
                continue
    return player_position_list

def return_player_team_dict():
    raw_player_team_list = return_player_position()
    player_team_list = list()
    print raw_player_team_list[:300]
    for n in range(0, len(raw_player_team_list), 30):
        player = raw_player_team_list[n + 1]
        position = raw_player_team_list[n + 2]
        team_id = raw_player_team_list[n + 4]
        if team_id == "TOT" or "-" in position or position == "G" or position == "F":
            continue
        else:
            raw_names = player.split(" ",)
            first_name = raw_names[0]
            last_name = raw_names[1]
            temp_dict = {
                'first_name': first_name,
                'last_name': last_name,
                'team_abbreviation': team_id
            }
            player_team_list.append(temp_dict)
    return player_team_list