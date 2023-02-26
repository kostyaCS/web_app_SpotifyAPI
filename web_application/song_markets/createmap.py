"""
This module include function that creates map with availiable
markets on folium and save it to the map.html
"""
from typing import List
import os
from pathlib import Path
import folium

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'song_markets')


def create_map(list_with_countries: List[str]):
    """
    Function that creates map availiable markets with user's artis(band) most popular song.

    :param list_with_countries: list with availiable markets
    :param type: list
    :return: None

    """
    mapobj = folium.Map(location=[30, 10], zoom_start=3)
    feature_group = folium.FeatureGroup(name="Availiable markets")
    folium.GeoJson(f'{STATIC_ROOT}/world.geojson', style_function=lambda x: {
        "fillColor": "#62F010"
        if x["properties"]["NAME"] in list_with_countries
        else "#FFFFFF", 'weight': 0.5
    }).add_to(feature_group)
    feature_group2 = folium.FeatureGroup(name='Unavailiable markets')
    folium.GeoJson(f'{STATIC_ROOT}/world.geojson', style_function=lambda x: {
        "fillColor": "#FF0000"
        if x["properties"]["NAME"] not in list_with_countries
else "#FFFFFF", 'weight': 0.5
    }).add_to(feature_group2)
    feature_group.add_to(mapobj)
    feature_group2.add_to(mapobj)
    folium.LayerControl().add_to(mapobj)
    mapobj.save(f"{STATIC_ROOT}/templates/song_markets/map.html")
