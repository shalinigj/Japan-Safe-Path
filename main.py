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
import altair as alt
import base64
from itertools import cycle

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

st.sidebar.markdown('<h1 style="margin-left:8%; color:#D19487 ">Nakagawa Dashboard for Safest Path </h1>',
                    unsafe_allow_html=True)

add_selectbox = st.sidebar.radio(
    "",
    ("Home", "About", "Features", "Safest Path", "Maps", "Visualizations", "Conclusion", "Team")
)

if add_selectbox == 'Home':
    
    LOGO_IMAGE = "omdena_japan_logo.jpg"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
          f"""
          <div class="container">
               <img class="logo-img" src="data:image/jpg;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    
    st.subheader('PROBLEM STATEMENT')
    
    st.markdown('Natural Disasters are problems in Japan, with risk of earthquakes, floods and tsunamis. Japan has well-developed \
        disaster response systems, but densely populated cities and narrow roads make managing the response difficult. By giving \
            individuals information about the safest ways from their homes and places of work, it will increase their awareness of \
                the surrounding area and improve their preparedness.', unsafe_allow_html=True)

elif add_selectbox == 'About':
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• collect satellite images and identify road characteristics', unsafe_allow_html=True) 
    st.markdown('• build a model for scoring the roads in terms of their suitability for use in emergency', unsafe_allow_html=True) 
    st.markdown('• build a pathfinding model from A to B, combining it with road characteristics', unsafe_allow_html=True) 
    st.markdown('• suggest safest path from A to B', unsafe_allow_html=True) 
    st.markdown('• publish interactive dashboards to display road characteristics and safest paths', unsafe_allow_html=True) 
    st.markdown('• arrange demonstration and publicise to local audiences', unsafe_allow_html=True) 
    
    st.markdown('<h4>Location Choosen</h4>', unsafe_allow_html=True)
    st.markdown('We had choosen "Nakagawa-Ku as our region of interest, which comes under Aichi prefecture of Nagoya City. It comes under Chubu region and \
        is the 4th densely populated city in Japan with high risk prone to disasters.',
                unsafe_allow_html=True)
    
    st.markdown('<h4>Developments Made</h4>', unsafe_allow_html=True)
    st.markdown('We had designed a model collecting data about the local roads from satellite images, classify them and indicate the safest \
        route to be taken from point A to point B and an interactive dashboard to display the safest route in a map.',
                unsafe_allow_html=True)
    st.markdown('By making individuals aware, it will improve their preparedness and it can be used within families to prepare disaster \
        response plans, depending on their circumstances. To be used by individuals, families and groups, and foreign residents who may \
            not understand local information. Further development will be covering more geographical areas and publicising on a local level.'
                , unsafe_allow_html=True)
    
elif add_selectbox == 'Features':

    st.subheader('PROJECT ENDORSEMENTS')

    st.markdown('• Safest route path to take at occurences of japan disasters', unsafe_allow_html=True)
    st.markdown('• Locates Shelters in Nakagawa Ward - Earthquakes, Tsunamis and Floods', unsafe_allow_html=True)
    st.markdown('• Visualizations to Check and Differentiate Parameters across the Nakagawa Ward', unsafe_allow_html=True)
    
elif add_selectbox == 'Safest Path':
    st.subheader('Find Safest Path')

    sentence = st.text_input('Input your current location:')

    # G_walk = ox.graph_from_place('Manhattan Island, New York City, New York, USA',
    #                          network_type='walk')

   # G_walk = joblib.load('G_walk.sav')

   # orig_node = ox.get_nearest_node(G_walk,
   #                                (40.748441, -73.985664))

   # dest_node = ox.get_nearest_node(G_walk,
   #                                (40.748441, -73.4))

   # route = nx.shortest_path(G_walk,
   #                         orig_node,
   #                          dest_node,
   #                          weight='length')

   # route_map = ox.plot_route_folium(G_walk, route)

   # folium_static(route_map, width=900)

elif add_selectbox == 'Maps':
    st.subheader('Maps')

    col1, col2 = st.columns(2)

    map_type = col1.selectbox(
        "Shelters",
        ('横手市 (Earthquakes)', '湯沢市 (Tsunamis)', '湯沢市 (Floods)')
        
    )
     
    ward_type = col2.selectbox(
        "Ward",
        ( '横手市 (Nakagawa Ward)', '横手市 (Midori Ward)'
        )
       
    )
      
    
    if st.button('Search'):
                   
        if map_type == '横手市 (Earthquakes)':            
            map_data = pd.read_csv('nakagawa_earthquake_shelters.csv')
        elif map_type == '湯沢市 (Tsunamis)':
            map_data = pd.read_csv('nakagawa_tsunami_shelters.csv')
        elif map_type == '湯沢市 (Floods)':
            map_data = pd.read_csv('nakagawa_flood_shelters.csv')
    
    
        #ward = ward_type
        st.write(ward_type)
        #ward_split = str(ward[1]).replace("("," ")
       
        
        details = map_data[map_data['ward']==ward_type]
      
        coordinates = {
        
          '中川区(Nakagawa Ward)': [35.1392027, 136.7778013],
            '緑区(Midori Ward)': [35.0852, 136.9708]
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

       #london_location = [35.183334,136.899994]

       #m = folium.Map(location=london_location, zoom_start=15)
        folium_static(m, width=900)
        
        
elif add_selectbox == 'Visualizations':
    
    
    #image1 = ['one.JPG']
    #st.image("one.jpg", use_column_width=True, caption=["Chocolate"]) * len(image))
    st.markdown('<h4>Japan Earthquake Zoning Areas</h4>', unsafe_allow_html=True)
    st.image("Japan_Earthquakes_Zoning.png", width=450)
    st.markdown('<h4>Nakagawa Shelter Maps</h4>', unsafe_allow_html=True)
    st.image("Nakagawa_Shelter_Maps.png", width=450)
    st.markdown('<h4>Nakagawa Building Density Score</h4>', unsafe_allow_html=True)
    st.image("Nakagawa_Building_Density_Score.png", width=450)
    st.markdown('<h4>Nakagawa Building Distance Risk Score</h4>', unsafe_allow_html=True)
    st.image("Nakagawa_Building_Distance_Risk_Score.png", width=450)
   
    #st.image("one.jpg", width=400, caption=["Chocolate"])

    #filteredImages = ['one.JPG', 'one.JPG', 'one.JPG', 'one.JPG'] # your images here
    #caption = ['i want one', 'I want two', 'I want three', 'I want four'] # your caption here
    #cols = cycle(st.columns(2)) # st.columns here since it is out of beta at the time I'm writing this
    #for idx, filteredImage in enumerate(filteredImages):
    #    next(cols).image(filteredImage, width=400, caption=caption[idx])
        
    #image2 = ['P2100483.JPG']
    #st.image(image2, use_column_width=True, caption=["some generic text"] * len(image2))
    #image3 = ['P2100483.JPG']
    #st.image(image3, use_column_width=True, caption=["some generic text"] * len(image3))
    #image4 = ['P2100483.JPG']
    #st.image(image4, use_column_width=True, caption=["some generic text"] * len(image4))

    
elif add_selectbox == 'Conclusion':
    
    st.subheader('PROJECT SUMMARY')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('Write Project Summary here', unsafe_allow_html=True) 
    
    st.subheader('CONCLUSION')
    
    st.markdown('Write Conclusion here', unsafe_allow_html=True)
    
    
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
                
