import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import json
from pandas.io.json import json_normalize #package for flattening json in pandas df
from baseball_id import Lookup

def get_player_splits(fangraphs_id, year): # get individual leaderboard
    url = f"https://cdn.fangraphs.com/api/players/splits?playerid={fangraphs_id}&position=OF&season={year}&split=&z=11"

    page = requests.get(url)
    df = pd.read_json(page.text)

    return df

def clean_html(list_): # clean html in df specified column
    temp_list = []
    for html_ in list_:
        temp_text = BeautifulSoup(html_, 'html.parser')
        temp_list.append(temp_text.text)
    return temp_list

def get_player_gamelogs(fangraphs_id, position): # get individual leaderboard
    url = f"https://cdn.fangraphs.com/api/players/game-log?playerid={fangraphs_id}&position={position}&type=0&season=&gds=&gde=&z=1"

    json = requests.get(url)
    df = pd.read_json(json.text[7:-1])
    df['Date'] = clean_html(df['Date'])

    return df

if __name__ == "__main__":
    print("getting player splits...\n")
    print("Juan Soto 2020 splits")
    soto_splits = get_player_splits("20123","2020")
    print(soto_splits)

    print("getting player gamelogs...\n")
    print("Juan Soto 2020 gamelogs")
    soto_gamelog = get_player_gamelogs("20123","OF")
    print(soto_gamelog)
