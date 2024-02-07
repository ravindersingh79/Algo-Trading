import streamlit as st
import requests
import pandas as pd
import time
from jugaad_data.nse import stock_df
from datetime import date, timedelta
from ta.momentum import RSIIndicator
import pandas as pd
import requests
import seaborn as sns
from datetime import date
from jugaad_data.nse import stock_df
import numpy as np
from datetime import date, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from ta.trend import ADXIndicator
from streamlit.components.v1 import html
import json

sidebar_option = st.sidebar.selectbox("Select an Option", ["NIFTY50", "INDICATORS"])

if sidebar_option =="NIFTY50":
    st.header('NIFTY50')

    def get_top_gainers():
        try:
            headers = {'User-Agent': 'your_user_agent'}
            url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                top_gainers = data.get('data', [])

                if top_gainers:
                    end = pd.DataFrame(top_gainers)
                    return list(end['symbol'].loc[1:])
                else:
                    st.text("No data found in the 'data' key.")
                    return None
            else:
                st.text(f"Failed to retrieve data. Status code: {response.status_code}")
                return None
        except TypeError as e:
            st.error(f"Error: {e}")
            return None


    # Function to update dropdown options
    def auto_update_dropdown():
        while st.session_state.running:
            symbols = get_top_gainers()
            if symbols:
                st.session_state.dropdown_options = symbols
            time.sleep(10)

    if "dropdown_options" not in st.session_state:
        st.session_state.dropdown_options = []





    selected_symbol = st.selectbox("Select a symbol:", st.session_state.dropdown_options, key="second_selectbox")

    refresh_button = st.button("Refresh Dropdown")
    if refresh_button:
        st.text("Fetching data... Please wait.")
        st.session_state.dropdown_options = get_top_gainers()
        if st.session_state.dropdown_options is not None:
            st.text("Data fetched successfully!")


    def stock_fetch(symbol):
        end_date = date.today()
        start_date = end_date - timedelta(days=300)
        tata_motors_stock_df = stock_df(symbol, from_date=start_date, to_date=end_date, series="EQ")
        tata_motors_stock_df = tata_motors_stock_df.sort_values(by='DATE', ascending=True)
        tata_motors_stock_df = tata_motors_stock_df.reset_index().drop(['index'], axis=1)
        tata_motors_stock_df['DATE'] = pd.to_datetime(tata_motors_stock_df['DATE'])
        tata_motors_stock_df1 = tata_motors_stock_df.drop(['SYMBOL', 'SERIES', '52W H', '52W L', 'LTP', 'VWAP'], axis=1)
        tata_motors_stock_df1 = tata_motors_stock_df1.set_index('DATE')
        return tata_motors_stock_df1


    data = stock_fetch(selected_symbol)

    st.write(data)

if sidebar_option == "INDICATORS":
    st.header('INDICATORS')

    def get_top_gainers():
        try:
            headers = {'User-Agent': 'your_user_agent'}
            url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                top_gainers = data.get('data', [])

                if top_gainers:
                    end = pd.DataFrame(top_gainers)
                    return list(end['symbol'].loc[1:])
                else:
                    st.text("No data found in the 'data' key.")
                    return None
            else:
                st.text(f"Failed to retrieve data. Status code: {response.status_code}")
                return None
        except TypeError as e:
            st.error(f"Error: {e}")
            return None


    # Function to update dropdown options
    def auto_update_dropdown():
        while st.session_state.running:
            symbols = get_top_gainers()
            if symbols:
                st.session_state.dropdown_options = symbols
            time.sleep(10)

    if "dropdown_options" not in st.session_state:
        st.session_state.dropdown_options = []




    # Display the dropdown
    selected_symbol = st.selectbox("Select a symbol:", st.session_state.dropdown_options, key="second_selectbox")

    refresh_button = st.button("Refresh Dropdown")
    if refresh_button:
        st.text("Fetching data... Please wait.")
        st.session_state.dropdown_options = get_top_gainers()
        if st.session_state.dropdown_options is not None:
            st.text("Data fetched successfully!")


    def stock_fetch(symbol):
        end_date = date.today()
        start_date = end_date - timedelta(days=200)
        tata_motors_stock_df = stock_df(symbol, from_date=start_date, to_date=end_date, series="EQ")
        tata_motors_stock_df = tata_motors_stock_df.sort_values(by='DATE', ascending=True)
        tata_motors_stock_df = tata_motors_stock_df.reset_index().drop(['index'], axis=1)
        tata_motors_stock_df['DATE'] = pd.to_datetime(tata_motors_stock_df['DATE'])
        tata_motors_stock_df1 = tata_motors_stock_df.drop(['SYMBOL', 'SERIES', '52W H', '52W L', 'LTP', 'VWAP'], axis=1)
        tata_motors_stock_df1 = tata_motors_stock_df1.set_index('DATE')
        return tata_motors_stock_df1


    data = stock_fetch(selected_symbol)

    st.write(data)


    def moving_average1(data, column='CLOSE'):
        ds = pd.DataFrame()
        ds['9_days'] = data[column].rolling(9).mean()
        ds['21_days'] = data[column].rolling(21).mean()
        ds['signal'] = np.where(ds['9_days'] > ds['21_days'], 1, 0)
        ds['signal'] = np.where(ds['9_days'] < ds['21_days'], -1, ds['signal'])
        ds['return'] = np.log(data[column]).diff()
        ds['system_return'] = ds['signal'] * ds['return']
        ds['entry'] = ds['signal'].diff()
        ds['CLOSE'] = data[column]
        return ds


    def rsi_indicator(data, column='CLOSE'):

        rsi_indicator = RSIIndicator(data[column])
        rsi_value = rsi_indicator.rsi()
        return rsi_value


    def adx(data, column1='HIGH', column2='LOW', column3='CLOSE'):
        fd = pd.DataFrame()
        adx_period = 14
        adx_indicator = ADXIndicator(high=data[column1], low=data[column2], close=data[column3], window=adx_period)
        fd['ADX'] = adx_indicator.adx()
        fd['Plus_DI'] = adx_indicator.adx_pos()
        fd['Minus_DI'] = adx_indicator.adx_neg()
        return fd


    def calculate_bollinger_bands(data, window=20, num_std=2):
        fg = pd.DataFrame()
        fg['Middle_Band'] = data['CLOSE'].rolling(window=window).mean()
        fg['Std_Dev'] = data['CLOSE'].rolling(window=window).std()
        fg['Upper_Band'] = fg['Middle_Band'] + (num_std * fg['Std_Dev'])
        fg['Lower_Band'] = fg['Middle_Band'] - (num_std * fg['Std_Dev'])
        fg['CLOSE'] = data['CLOSE']

        return fg


    if st.button("Run INDICATORS"):

        ds = moving_average1(data, column='CLOSE')
        rsi = rsi_indicator(data, column='CLOSE')
        sd = adx(data, column1='HIGH', column2='LOW', column3='CLOSE')
        fg = calculate_bollinger_bands(data, window=20, num_std=2)

        # PLOT MOVING AVERAGE
        trace_close = go.Scatter(x=ds.index, y=ds['CLOSE'], mode='lines', name='Close')
        trace_9_days = go.Scatter(x=ds.index, y=ds['9_days'], mode='lines', name='9-day')
        trace_21_days = go.Scatter(x=ds.index, y=ds['21_days'], mode='lines', name='21-day')
        trace_entry_buy = go.Scatter(x=ds.loc[ds['entry'] == 2].index, y=ds['9_days'][ds['entry'] == 2],
                                     mode='markers', marker=dict(color='green', size=12), name='Buy Entry')
        trace_entry_sell = go.Scatter(x=ds.loc[ds['entry'] == -2].index, y=ds['21_days'][ds['entry'] == -2],
                                      mode='markers', marker=dict(color='red', size=12), name='Sell Entry')

        # Create layout
        layout = go.Layout(title='Moving Average Analysis Chart', showlegend=True, width=800, height=600)

        # Create figure
        fig = go.Figure(data=[trace_close, trace_9_days, trace_21_days, trace_entry_buy, trace_entry_sell],
                        layout=layout)

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Another PLOT

        trace_rsi = go.Scatter(x=rsi.index, y=rsi.values, mode='lines', name='RSI')

        # Create traces for horizontal lines
        trace_overbought = go.Scatter(x=rsi.index, y=[60] * len(rsi), mode='lines', name='Overbought (60)',
                                      line=dict(color='red'))
        trace_oversold = go.Scatter(x=rsi.index, y=[40] * len(rsi), mode='lines', name='Oversold (40)',
                                    line=dict(color='green'))

        # Create layout
        layout = go.Layout(
            title='Modified RSI with Overbought and Oversold Levels',
            xaxis=dict(title='Date'),
            yaxis=dict(title='RSI Value'),
        )

        # Combine traces and layout into a figure
        fig1 = go.Figure(data=[trace_rsi, trace_overbought, trace_oversold], layout=layout)

        # Show the plot
        st.plotly_chart(fig1)

        # another plot

        trace_rsi = go.Scatter(x=rsi.index, y=rsi.values, mode='lines', name='RSI')

        # Create traces for horizontal lines
        trace_overbought = go.Scatter(x=rsi.index, y=[70] * len(rsi), mode='lines', name='Overbought (70)',
                                      line=dict(color='red'))
        trace_oversold = go.Scatter(x=rsi.index, y=[30] * len(rsi), mode='lines', name='Oversold (30)',
                                    line=dict(color='green'))

        # Create layout
        layout = go.Layout(
            title='RSI with Overbought and Oversold Levels',
            xaxis=dict(title='Date'),
            yaxis=dict(title='RSI Value'),
        )

        # Combine traces and layout into a figure
        fig2 = go.Figure(data=[trace_rsi, trace_overbought, trace_oversold], layout=layout)

        # Show the plot
        st.plotly_chart(fig2)

        # another plot
        trace_adx = go.Scatter(x=sd.index, y=sd['ADX'], mode='lines', name='ADX', line=dict(color='white'))
        trace_plus_di = go.Scatter(x=sd.index, y=sd['Plus_DI'], mode='lines', name='Plus_DI', line=dict(color='green'))
        trace_minus_di = go.Scatter(x=sd.index, y=sd['Minus_DI'], mode='lines', name='Minus_DI', line=dict(color='red'))

        # Create a trace for the Trend Strength Threshold
        trace_threshold = go.Scatter(x=sd.index, y=[25] * len(sd), mode='lines', name='Trend Strength Threshold',
                                     line=dict(color='red'))

        # Create layout
        layout = go.Layout(
            title='ADX Indicator with Trend Strength Threshold',
            xaxis=dict(title='Date'),
            yaxis=dict(title='ADX Value'),
        )

        # Combine traces and layout into a figure
        fig4 = go.Figure(data=[trace_adx, trace_plus_di, trace_minus_di, trace_threshold], layout=layout)

        # Show the plot
        st.plotly_chart(fig4)

        # plotly
        trace_close = go.Scatter(x=fg.index, y=fg['CLOSE'], mode='lines', name='Closing Price', line=dict(color='blue'))
        trace_middle_band = go.Scatter(x=fg.index, y=fg['Middle_Band'], mode='lines', name='Middle Band',
                                       line=dict(color='black'))
        trace_upper_band = go.Scatter(x=fg.index, y=fg['Upper_Band'], mode='lines', name='Upper Band',
                                      line=dict(color='red'))
        trace_lower_band = go.Scatter(x=fg.index, y=fg['Lower_Band'], mode='lines', name='Lower Band',
                                      line=dict(color='green'))

        # Create layout
        layout = go.Layout(
            title='Bollinger Bands',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price'),
        )

        # Combine traces and layout into a figure
        fig6 = go.Figure(data=[trace_close, trace_middle_band, trace_upper_band, trace_lower_band], layout=layout)

        # Show the plot
        st.plotly_chart(fig6)

























