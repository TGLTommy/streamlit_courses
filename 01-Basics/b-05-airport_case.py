import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
# pip install streamlit_lottie
st.header("Airport Example")
st.subheader("根据机场所在的经纬度，计算两两之间的距离")

# 1. 动态图设置
st.markdown("### 1. 动态图设置")
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

airplane_gif = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
st_lottie(airplane_gif, speed=1.5, height=200, width=200)
# 动态图下载：https://lottiefiles.com/

# 2. 输入密码验证
st.markdown("### 2. 输入密码验证")
password = st.text_input("请输入6位数字密码")
if password != "123456":
    st.write("密码错误")
    st.stop()

# 3. 指定一个机场，根据候选所有机场的经纬度，计算两者之间的距离，由远及近进行排序
st.markdown("### 3. 根据经纬度计算距离")
st.markdown("""
1、问题描述: 指定一个机场，根据候选所有机场的经纬度，计算两者之间的距离，由远及近进行排序
2、执行步骤：
    ① 加载数据集
    ② 实施距离算法
    ③ 计算所有机场之间的距离
    ③ 根据距离排序（由远及近）
""")

# 4. 在页面上显示以下代码块
st.markdown("### 4. 在页面上显示代码块（根据经纬度计算距离）")
with st.echo():
    df = pd.read_csv("01-Basics/data/airport_location.csv")
st.write(df)
"""半正弦 Haversine distance \n
半正弦距离是给定经度和纬度的球体上两点之间的距离。它与欧几里得距离非常相似，因为它计算两点之间的最短线。主要区别在于不可能有直线，因为这里的假设是两点在一个球面上。
"""
st.image("01-Basics/data/haversine.png")

with st.echo():
    from math import radians, sin, cos, atan2, sqrt
    def haversine_distance(long1, lat1, long2, lat2, degrees=False):
        # 角度 vs 弧度
        if degrees:
            long1 = radians(long1)
            lat1 = radians(lat1)
            long2 = radians(long2)
            lat2 = radians(lat2)
        # 半正弦计算距离公式
        a = sin((lat2 - lat1) / 2)**2 + cos(lat1) * cos(lat2) * sin((long2 - long1)/2)**2
        b = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = 6371 * b # 单位：公里
        return distance
# 测试函数功能
st.markdown("### 5. 测试距离：半正弦函数测试，根据经纬度计算两点之间的距离")
long1 = st.number_input("经度-1: ", value=2.55)
long2 = st.number_input("经度-2: ", value=172.00)
lat1 = st.number_input("维度-1: ", value=49.01)
lat2 = st.number_input("维度-2: ", value=-43.48)
test_distance = haversine_distance(long1=long1, long2=long2, lat1=lat1, lat2=lat2)
st.write("两点之间的距离是: ", int(test_distance),"公里")

st.markdown("### 6. 根据输入的机场编号，计算与其它机场之间的距离")
airport_code = st.selectbox("选择机场编号: ",
                            df['Airport Code'].unique())

def get_distances(df, airport_code="CDG"):
    # ① 根据输入的 airport_code，获取到对应的经纬度
    temp_df = df[df['Airport Code']==airport_code]
    temp_lat = temp_df['Lat'].values[0] # 纬度
    temp_long = temp_df['Long'].values[0] # 经度
    st.write("机场编号: {}, 输入的经度: {}, 纬度: {}".format(airport_code, temp_long, temp_lat))
    # ② 获取其它机场的经纬度
    others_df = df[df['Airport Code']!=airport_code]
    # ③ 计算两者之间的距离
    others_df['distance'] = others_df.apply(lambda x: haversine_distance(long1=temp_long,
                                                                         lat1=temp_lat,
                                                                         long2=x.Long,
                                                                         lat2=x.Lat,
                                                                         degrees=True),
                                            axis=1)
    # ④ 根据距离排序
    return others_df.sort_values(by='distance', ascending=False)

result_df = get_distances(df, airport_code=airport_code)
st.write(result_df)

