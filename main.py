import datetime
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib

import osmnx as ox
import shapely.wkt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time

from folium.features import DivIcon
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Nakagawa Dashboard for Safest Path during Earthquakes",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.markdown('<h1 style="margin-left:8%; color:#1a5276">Nakagawa Dashboard for Safest Path </h1>',
                    unsafe_allow_html=True)

add_selectbox = st.sidebar.radio(
    "",
    ("Home", "About", "Features", "Safest Path", "Maps", "Visualization", "Conclusion", "Team")
)

if add_selectbox == 'About':
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>The Background</h4>', unsafe_allow_html=True)
    st.markdown('Natural Disasters are problems in Japan, with risk of earthquakes, floods and tsunamis. Japan has well-developed \
        disaster response systems, but densely populated cities and narrow roads make managing the response difficult. By giving \
            individuals information about the safest ways from their homes and places of work, it will increase their awareness of \
                the surrounding area and improve their preparedness.', unsafe_allow_html=True)
    st.markdown('<h4>The Problem</h4>', unsafe_allow_html=True)
    st.markdown('Design a model collecting data about the local roads from satellite images, classify them and indicate the safest \
        route to be taken from point A to point B. Design an interactive dashboard to display the safest route in a map.',
                unsafe_allow_html=True)
    st.markdown('By making individuals aware, it will improve their preparedness and it can be used within families to prepare disaster \
        response plans, depending on their circumstances. To be used by individuals, families and groups, and foreign residents who may \
            not understand local information. Further development will be covering more geographical areas and publicising on a local level.'
                , unsafe_allow_html=True)

elif add_selectbox == 'Safest Path':
    st.subheader('Find Safest Path')

    sentence = st.text_input('Input your current location:')

    # G_walk = ox.graph_from_place('Manhattan Island, New York City, New York, USA',
    #                          network_type='walk')

    G_walk = joblib.load('G_walk.sav')

    orig_node = ox.get_nearest_node(G_walk,
                                    (40.748441, -73.985664))

    dest_node = ox.get_nearest_node(G_walk,
                                    (40.748441, -73.4))

    route = nx.shortest_path(G_walk,
                             orig_node,
                             dest_node,
                             weight='length')

    route_map = ox.plot_route_folium(G_walk, route)

    folium_static(route_map, width=900)

elif add_selectbox == 'Maps':
    st.subheader('Maps')

    col1, col2 = st.columns(2)

    map_type = col1.selectbox(
        "Shelters",
        ('横手市 (Earthquakes)', '湯沢市 (Tsunamis)', '湯沢市 (Floods)')
         )

    ward_type = col2.selectbox(
        "Ward",
        ('横手市 (Nakagawa Ward)')
         )

    if st.button('Search'):
        if map_type == 'Earthquakes':
            map_data = pd.read_csv('nakagawa_earthquake_shelters.csv')
        elif map_type == 'Tsunamis':
            map_data = pd.read_csv('nakagawa_tsunami_shelters.csv')
        elif map_type == 'Floods':
            map_data = pd.read_csv('nakagawa_flood_shelters.csv')

        ward = ward_type.split(" ")

        details = map_data[map_data['Ward'] == ward[0]]

        coordinates = {
            '中川区 (Nakagawa Ward)': [35.139288, 136.8128218]
        }

        m = folium.Map(location=coordinates[ward_type], zoom_start=10)
        for index, row in details.iterrows():
            if row['geometry'].startswith("POINT"):
                geometry = shapely.wkt.loads(row['geometry'])
            else:
                p = shapely.wkt.loads(row['geometry'])
                geometry = p.centroid

            folium.Marker(
                [geometry.y, geometry.x], popup=row['display_name'],
            ).add_to(m)

        # london_location = [35.183334,136.899994]

        # m = folium.Map(location=london_location, zoom_start=15)
        folium_static(m, width=900)

elif add_selectbox == 'Team':
    st.subheader('Collaborators')

    st.markdown('<a href="https://www.linkedin.com/in/mkmanolova/">Monika Manolova</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/prathima-kadari/">Prathima Kadari</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/avinash-mahech/">Avinash Mahech</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/armielyn-obinguar-9229561b0/">Armielyn Obinguar</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/shalini-gj-6a006712/">Shalini GJ</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/rhey-ann-magcalas-47541490/">Rhey Ann Magcalas</a>',
                unsafe_allow_html=True)
    st.markdown('<a href="https://www.linkedin.com/in/deepali-bidwai/">Deepali Bidwai</a>',
                unsafe_allow_html=True)

    st.subheader('Project Manager')

    st.markdown('<a href="https://www.linkedin.com/in/galina-naydenova-msc-fhea-b89856196/">Galina Naydenova</a>', unsafe_allow_html=True)
                
