import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import json
from pandas.io.json import json_normalize #package for flattening json in pandas df
from baseball_id import Lookup

pitcher_leaderboards_url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=&page=1_100'
pitcher_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=0&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
pitcher_advanced_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
pitcher_batted_ball_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=2&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
pitcher_win_probability_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=3&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
pithcer_pitch_type_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=4&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
pitcher_plate_discipline = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=5&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"

hitter_leaderboards_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=&page=1_500"
hitter_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=0&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
hitter_advanced_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
hitter_batted_ball_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=2&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
hitter_win_probability_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=3&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
hitter_pitch_type_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=4&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
hitter_plate_discipline = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=5&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"


leaderboards_urls = [ pitcher_leaderboards_url, pitcher_stats_url, pitcher_advanced_stats_url, pitcher_batted_ball_url,
                    pitcher_win_probability_url, pithcer_pitch_type_url, pitcher_plate_discipline, hitter_leaderboards_url,
                    hitter_stats_url, hitter_advanced_stats_url, hitter_batted_ball_url, hitter_win_probability_url,
                    hitter_pitch_type_url, hitter_plate_discipline ]

leaderboards_names = [ "pitcher_leaderboards_", "pitcher_stats_", "pitcher_advanced_stats_", "pitcher_batted_ball_",
                    "pitcher_win_probability_", "pithcer_pitch_type_", "pitcher_plate_discipline_", "hitter_leaderboards_",
                    "hitter_stats_", "hitter_advanced_stats_", "hitter_batted_ball_", "hitter_win_probability_",
                    "hitter_pitch_type_", "hitter_plate_discipline_" ]


def get_headers(table): # get table headers
    header_cols = table.find_all('th') # find headers HTML

    headers = []
    for line in header_cols[1:]: # iterate through Headers
        headers.append(line.get_text()) # get individual header text

    return headers # return list of headers


def get_leaderboard(url): # get individual leaderboard
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', attrs={'class': 'rgMasterTable'})
    tbodys = soup.find_all('tbody')

    rows = tbodys[1].find_all('tr') # get table lines

    headers = get_headers(table)

    player_stats = []
    for line in rows[:]:
        stats = line.find_all('td')# get stat html

        stat_line = []
        for stat in stats[1:]:
            stat_line.append(stat.get_text()) # get individual stat
        player_stats.append(stat_line) # append player stat line

    df = pd.DataFrame(player_stats, columns=headers) # make df
    return df

def get_leaderboards(urls): # get all leaderboards from list of urls
    leaderboards = []
    for url in urls:
        df = get_leaderboard(url)
        leaderboards.append(df)

    save_leaderboards(leaderboards)

    return leaderboards

def save_leaderboards(leaderboards):
    x = datetime.datetime.now()
    date = x.strftime("%Y-%m-%d") # get date in YYYY-MM-DD format

    for i,df in enumerate(leaderboards):
        filename = f"{leaderboards_names[i]+date}.csv"
        df.to_csv(filename,index=False)

def get_player_splits(fangraphs_id, year): # get individual leaderboard
    url = f"https://cdn.fangraphs.com/api/players/splits?playerid={fangraphs_id}&position=OF&season={year}&split=&z=11"

    page = requests.get(url)
    df = pd.read_json(page.text)

    return df


if __name__ == "__main__":

    # URLS are for the 2020 MLB Season
    pitcher_leaderboards_url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=&page=1_100'
    pitcher_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=0&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
    pitcher_advanced_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=1&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
    pitcher_batted_ball_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=2&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
    pitcher_win_probability_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=3&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
    pithcer_pitch_type_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=4&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"
    pitcher_plate_discipline = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=5&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_100"

    hitter_leaderboards_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=&page=1_500"
    hitter_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=0&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
    hitter_advanced_stats_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=1&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
    hitter_batted_ball_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=2&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
    hitter_win_probability_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=3&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
    hitter_pitch_type_url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=4&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"
    hitter_plate_discipline = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=5&season=2020&month=0&season1=2020&ind=0&team=0&rost=0&age=0&filter=&players=p2020-08-11&startdate=2020-01-01&enddate=2020-12-31&page=1_500"


    leaderboards_urls = [ pitcher_leaderboards_url, pitcher_stats_url, pitcher_advanced_stats_url, pitcher_batted_ball_url,
                        pitcher_win_probability_url, pithcer_pitch_type_url, pitcher_plate_discipline, hitter_leaderboards_url,
                        hitter_stats_url, hitter_advanced_stats_url, hitter_batted_ball_url, hitter_win_probability_url,
                        hitter_pitch_type_url, hitter_plate_discipline ]

    leaderboards_names = [ "pitcher_leaderboards_", "pitcher_stats_", "pitcher_advanced_stats_", "pitcher_batted_ball_",
                        "pitcher_win_probability_", "pithcer_pitch_type_", "pitcher_plate_discipline_", "hitter_leaderboards_",
                        "hitter_stats_", "hitter_advanced_stats_", "hitter_batted_ball_", "hitter_win_probability_",
                        "hitter_pitch_type_", "hitter_plate_discipline_" ]

    print("getting fangraphs leaderbaords...")
    leaderboards = get_leaderboards(leaderboards_urls) # get and save fangraph leaderboards
    save_leaderboards(leaderboards)
    print("leaderbaords downloaded, exiting program")
