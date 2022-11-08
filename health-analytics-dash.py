# -*- coding: utf-8 -*-
"""
Created on Monday November 7th 2022

@author: joshiggins
"""
# Importing full packages
import geopy
import openpyxl
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import leafmap.foliumap as leafmap

# Importing partial packages
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

st.set_page_config(page_title='TIPAC',  layout='wide', page_icon=':hospital:')

# this is the header
t1, t2 = st.columns((0.07,1)) # commented out and added the next line

t1.image('images/index.png', width = 120)
t2.title("Tool for Integrated Costing and Planning (TIPAC)")
t2.markdown(" **Phone:** 248-XXX-XXXX **| Website:** www.google.com **| Email:** joshiggins@deloitte.com")

tab1, tab2, tab3 = st.tabs(["Cost", "Financing", "Disease"])

# with tab1:

# with tab2:

with tab3:

    with st.spinner('Updating Report...'):

        health_df = pd.read_excel('health-analytics-data.xlsx', sheet_name='regions')
        region = st.selectbox('Choose Region', health_df, help='Filter report to show only one region')
        
        m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))
        
        # come back to this - fix it to work with key metrics
        todf = pd.read_excel('DataforMock.xlsx', sheet_name = 'metrics')
        to = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Total Outstanding')]   
        ch = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Current Handover Average Mins')]   
        hl = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Hours Lost to Handovers Over 15 Mins')]
        
        m1.write('')
        m2.metric(label ='Total Outstanding Handovers',value = int(to['Value']), delta = str(int(to['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
        m3.metric(label ='Current Handover Average',value = str(int(ch['Value']))+" Mins", delta = str(int(ch['Previous']))+' Compared to 1 hour ago', delta_color = 'inverse')
        m4.metric(label = 'Time Lost today (Above 15 mins)',value = str(int(hl['Value']))+" Hours", delta = str(int(hl['Previous']))+' Compared to yesterday')
        m1.write('')
        
        # Target Population
        g1, g2 = st.columns((1.5,1.5))

        hd_tp = pd.read_excel('health-analytics-data.xlsx', sheet_name='target_pop')
        hd_tp = hd_tp[hd_tp['Region']==region] 
        
        plot = go.Figure(data=[go.Bar(
            name = 'LF Lymphedema Management',
            y = hd_tp['LF Lymphedema Management'],
            x = hd_tp['District'],
        ),
                              go.Bar(
            name = 'Oncho Round 1',
            y = hd_tp['Oncho Round 1'],
            x = hd_tp['District'],
        ), 
                              go.Bar(
            name = 'SCH School Age Children',
            y = hd_tp['SCH School Age Children'],
            x = hd_tp['District'],
        ), 
                              go.Bar(
            name = 'SCH High Risk Adult',
            y = hd_tp['SCH High Risk Adult'],
            x = hd_tp['District'],
        ), 
        ])

        plot.update_layout(title_text="Target Population",
                           title_x=0,
                           margin= dict(l=0,r=10,b=10,t=30), 
                           xaxis_title='', 
                           yaxis_title='Target Population (Total Count)',
                           template='seaborn')
        
        g1.plotly_chart(plot, use_container_width=True)
        
        # Target Population Filler
        plot = go.Figure(data=[go.Bar(
            name = 'LF Lymphedema Management',
            y = hd_tp['LF Lymphedema Management'],
            x = hd_tp['District'],
        ),
                              go.Bar(
            name = 'Oncho Round 1',
            y = hd_tp['Oncho Round 1'],
            x = hd_tp['District'],
        ), 
                              go.Bar(
            name = 'SCH School Age Children',
            y = hd_tp['SCH School Age Children'],
            x = hd_tp['District'],
        ), 
                              go.Bar(
            name = 'SCH High Risk Adult',
            y = hd_tp['SCH High Risk Adult'],
            x = hd_tp['District'],
        ), 
        ])

        plot.update_layout(title_text="Target Population",
                           title_x=0,
                           margin= dict(l=0,r=10,b=10,t=30), 
                           xaxis_title='', 
                           yaxis_title='Target Population (Total Count)',
                           template='seaborn')
        
        g2.plotly_chart(plot, use_container_width=True) 

        # Choropleth
        test_df = pd.read_excel('health-analytics-data.xlsx', sheet_name='geo_data')
        test_df = test_df[test_df['Regions']==region]
        m = leafmap.Map(tiles="stamentoner", center=(10.984335, -10.964355), zoom=6)
        m.add_heatmap(
            test_df,
            latitude="Latitude",
            longitude="Longitude",
            value="Total Population",
            name="Total Population Map",
            radius=25,
        )
        m.to_streamlit(height=400)
        
        
        
        
        
        
        