"""
This module includes functions that works with SpotifyAPI
"""
import base64
import json
import os
from typing import List
from requests import post, get
from dotenv import load_dotenv
import pycountry


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token() -> str:
    """
    Function, that returns user token from the api.

    :return: user's token
    :return type: str

    """
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url ='https://accounts.spotify.com/api/token'

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data, timeout=10)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def get_auth_header(token: str):
    """
    Function, that returns authorization header.

    :param token: user's token
    :param type: str
    :return: authorization info
    :return type: dict

    """
    return {"Authorization": "Bearer " + token}


def search_for_artist(token: str, artist_name: str) -> dict:
    """
    Function, that returns dict, which indcludes all the information about
    given artist by it's name.

    :param token: user's token
    :param type: str
    :param artist_name: name of the artist(band)
    :param type: str
    :return: different kinds of info about artist
    :return type: dict

    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query

    result = get(query_url, headers=headers, timeout=10)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print('No artist with such name!')
        return None
    return json_result[0]


def get_songs_by_artist(token: str, artist_id: str) -> list:
    """
    Function, that returns top-10 artist's songs by his id.

    :param token: user's token
    :param type: str
    :param artist_id: id of user's artist(band)
    :param type: str
    :return: info about most popular artist's tracks
    :return type: list
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout=10)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_song_name(token: str, artist_id: str) -> str:
    """
    FUnction that returns the most popular artist's(band's) song

    :param token: user's token
    :param type: str
    :param artist_id: id of artist(band)
    :param type: str
    :return: the most popular artist's(band's) song
    :return type: str
    """
    songs = get_songs_by_artist(token, artist_id)
    return songs[0]['name']


def get_available_markets(token: str, song_id: str) -> list:
    """
    Function that search for availiable markets for artist's(band's) most popular song

    :param token: user's token
    :param type: str
    :param song_id: id of the most popular song
    :param type: str
    :return: availiable markets(countries)
    :return type: list
    """
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout=10)
    json_result = json.loads(result.content)
    return json_result['available_markets']


def get_list_of_countries(token: str, artist_id: str) -> List[str]:
    """
    Function that returns list with most popular countries(their full names)
    of the most popular artist's(band's) song

    :param token: user's token
    :param type: str
    :param artist_id: artist's id
    :param type: str
    :return: list with full name of countries
    :return type: list
    """
    songs = get_songs_by_artist(token, artist_id)
    list_of_countries =[]
    my_token = get_token()
    curr_song = songs[0]['id']
    for i in get_available_markets(my_token, curr_song):
        if pycountry.countries.get(alpha_2=i):
            list_of_countries.append(pycountry.countries.get(alpha_2=i).name)
    return list_of_countries
