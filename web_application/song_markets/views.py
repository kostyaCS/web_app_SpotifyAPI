import os
from django.shortcuts import render
from dotenv import load_dotenv
from . import apisearch
from . import createmap

load_dotenv()

client_id = "0922e09ab9f7417fa66b0eacd7b1abec"
client_secret = "f85877e6e0d64398a0694a274ca5a134"


def main(request):
    """
    Main function that works with user's request
    """
    if request.method == 'POST':
        artist = request.POST.get('artist-name')
        try:
            token = apisearch.get_token()
            artist_name = apisearch.search_for_artist(token, artist)
            list_countries = apisearch.get_list_of_countries(token, artist_name["id"])
            song_name = apisearch.get_song_name(token, artist_name["id"])
            createmap.create_map(list_countries)
        except TypeError:
            return render(request, 'song_markets/error.html', {})
        return render(request, 'song_markets/search.html', {"song_name": song_name})
    return render(request, 'song_markets/main.html', {})


def map_page(request):
    """
    Function, that redirect user to the map.hmtl
    """
    return render(request, 'song_markets/map.html', {})
