# 官网案例

import pandas as pd
import streamlit as st
import numpy as np

st.title("Uber pickups in NYC")

DATE_COLUMN = "date/time"
DATA_PATH = "data/uber-raw-data-sep14.csv"

# 1、加载数据
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_PATH, nrows=nrows)
    data.rename(lambda x:str(x).lower(), axis='columns', inplace=True) # 列名转换为小写
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) # 日期类型转换
    return data

data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Loading data is done!")

# 2、查看数据
st.subheader("Raw Data")
st.write(data.head())

# 3、绘制直方图（每小时的载客量）
st.subheader("Number of pickups by hour")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour,
                           bins=24,
                           range=(0,24))[0]
st.bar_chart(hist_values)

# 4、在地图上绘制
st.subheader("Map of all pickups")
st.map(data)

# 5、 查看某个时刻的乘客分布
hour_to_filter = st.slider('hour', 0, 23, 17) # 0-23点，默认 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

