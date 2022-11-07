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
        
        # Metrics setting and rendering
        hosp_df = pd.read_excel('DataforMock.xlsx',sheet_name = 'Hospitals')
        hosp = st.selectbox('Choose Hospital', hosp_df, help = 'Filter report to show only one hospital')

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
        
        fgdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'Graph')
        fgdf = fgdf[fgdf['Hospital Attended']==hosp] 

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
                        xaxis_title='District', 
                        yaxis_title='Target Population (Total Count)',
                        template='seaborn')
        
        g1.plotly_chart(plot, use_container_width=True)
        
        # Predicted Number of Arrivals
        fcst = pd.read_excel('DataforMock.xlsx',sheet_name = 'Forecast')
        
        fcst = fcst[fcst['Hospital Attended']==hosp]
        
        fig = px.bar(fcst, x = 'Arrived Destination Resolved', y='y', template = 'seaborn')
        fig.update_traces(marker_color='#7A9E9F')        
        fig.update_layout(title_text="Predicted Number of Arrivals",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
        
        g2.plotly_chart(fig, use_container_width=True)  

        g3, g4 = st.columns((3,1))

        # Choropleth
        test_df = pd.read_excel('health-analytics-data.xlsx', sheet_name='geo_data')
        px.set_mapbox_access_token("pk.eyJ1Ijoiam9laGlnZ2kxNzU4IiwiYSI6ImNsOWZ1NGkzZDJubnIzeGw5NHAxcjZyeDQifQ.OxUPPPmwro-Vm_58P1B3UQ")
        fig = px.scatter_mapbox(test_df, 
                                lat="Latitude", 
                                lon="Longitude", 
                                color="Total Population", 
                                size="Total Population",
                                color_continuous_scale=px.colors.cyclical.IceFire, 
                                size_max=15, 
                                zoom=5)
        fig = fig.show()

        g3.plotly_chart(fig, use_container_width=True) 
        
# Contact Form
with st.expander("Contact us"):
    with st.form(key='contact', clear_on_submit=True):
        
        email = st.text_input('Contact Email')
        st.text_area("Query","Please fill in all the information or we may not be able to process your request")  
        
        submit_button = st.form_submit_button(label='Send Information')
        
        
        
        
        
        
        
        
        
        