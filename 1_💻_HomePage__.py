import streamlit as st
import yfinance as yf
import pandas as pd

# sayfa başlığı

st.set_page_config(page_title="Dashboard",


# sayfa tasarımı
                   
                   page_icon=":bar_chart:", layout="wide")
st.markdown('<h1 style="text-align:center; color:lime; font-weight:bold;text-decoration:underline;">Top Finace List </h1>',unsafe_allow_html=True)
st.title(":bar_chart:")
def load_data(fpath):
    data=pd.read_csv(fpath)
    return list(data)

# Veri Çekme ve tarih filtreleme

tickers=load_data("data.csv")
st.text("Input asset ⬇️")
input2=st.text_input(":orange[Input your assets]",placeholder="TSLA BTC-USD")
start=st.date_input(":orange[Select Start Date 🗓️]",value=pd.to_datetime("2020-01-01"))
end=st.date_input(":orange[Select End Date 🗓️]", value=pd.to_datetime("today"))


# veri çekme fonksiyonu

def relativeret(df):
    rel=df.pct_change()
    cumret=(1+rel).cumprod()-1
    cumret=cumret.fillna(0)
    return cumret
       

# varlık ismi alma ve fonksiyonu çağırma

if len(input2)>0:
    df=relativeret(yf.download(input2,start,end)["Adj Close"])
    st.line_chart(df)
else:
    st.write("Please input an asset ")