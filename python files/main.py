import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
import webbrowser
from plotly import graph_objs as go
from PIL import Image

st.header("I.N.V.E.S.T.O")
# image = Image.open('https://33.media.tumblr.com/71cfd3332d2ef2dd0e166572f4a5d7b4/tumblr_nmegikHkri1tg7xcdo1_500.gif')
# st.image(image, caption='Sunrise by the mountains',width='500px')

st.sidebar.header("STOCKS")
option = st.sidebar.selectbox("Dashboard",('Stock-Data','Prediction'))
st.sidebar.subheader(option)
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())

# Retrieving tickers data
ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)

if option == 'Stock-Data':

     # Select ticker symbol
    tickerData = yf.Ticker(tickerSymbol)  # Get ticker data
    tickerDf = tickerData.history(period='1d', start=start_date,
                                  end=end_date)  # get the historical prices for this ticker

    # Ticker information

    # Ticker data
    st.header('**Ticker data**')
    st.write(tickerDf)

    # Bollinger bands
    st.header('**Bollinger Bands**')
    qf = cf.QuantFig(tickerDf, title='First Quant Figure', legend='top', name='GS')
    qf.add_bollinger_bands()
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)

 #go-through-link
    st.subheader('our trusted links')
    LINKS = ('zerodha', '5paisa', 'groww', 'ETmoney')
    selected_LINK = st.selectbox('Select you required trading-place', LINKS)

    if selected_LINK == 'zerodha':
        if st.button('Go to Zerodha'):
            url = 'https://zerodha.com/'
            webbrowser.open_new_tab(url)

    if selected_LINK == '5paisa':
        if st.button('Go to 5paisa'):
            url = 'https://www.5paisa.com/'
            webbrowser.open_new_tab(url)

    if selected_LINK == 'groww':
        if st.button('Go to Groww'):
            url = 'https://groww.in/'
            webbrowser.open_new_tab(url)

    if selected_LINK == 'ETmoney':
        if st.button('Go to ETmoney'):
            url = 'https://www.etmoney.com/'
            webbrowser.open_new_tab(url)



if option == 'Prediction':

    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365


    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, start_date, end_date)
        data.reset_index(inplace=True)
        return data


    data_load_state = st.text('Loading data...')
    data = load_data(tickerSymbol)
    data_load_state.text('Loading data... done!')


    # Predict forecast with Prophet.
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)
