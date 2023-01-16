
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests

# pip install streamlit-lottie

st.title("案例：分析GoodReads上的阅读习惯")
st.subheader("----- 以下为案例分析流程 --------")

# 1、动态图设置
st.markdown("### 1. 动态图设置")
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

file_url = "https://assets4.lottiefiles.com/packages/lf20_Ux9vQsfwL7.json"
lottie_gif = load_lottieurl(file_url)
st_lottie(lottie_gif,
          speed=1,
          height=200,
          width=200)

# 2、上传数据文件
st.markdown("### 2. 上传数据文件")
upload_file = st.file_uploader(
    label = "请上传Goodreads数据文件csv"
)

if upload_file is None:
    # 如果为空，则使用默认的数据集
    df = pd.read_csv("data/goodreads_history.csv")
    st.write("*** 默认数据集分析 ***")
else:
    df = pd.read_csv(upload_file)
    st.write("*** 个人数据集分析 ***")

# 3、显示默认的前5行数据
st.markdown("### 3. 默认显示前5行")
st.write(df.head())

# 4、统计每一年读了多少本书
st.markdown("### 4. 统计每一年读了多少本书")
df['year finished'] = pd.to_datetime(df['Date Read']).dt.year
# 根据 year finished 分组
books_per_year = df.groupby('year finished')['Book Id'].count().reset_index()
# 重置列名
books_per_year.columns = ['year finished', 'count']
st.write(books_per_year)
# 可视化
fig1 = px.bar(books_per_year,
             x = 'year finished',
             y = 'count',
             title = 'books finished per year')
st.plotly_chart(fig1)


# 5、统计读完一本书需要花多长时间
st.markdown("### 5. 统计读完一本书需要花多长时间")
df['read period'] = (pd.to_datetime(df['Date Read']) - pd.to_datetime(df['Date Added'])).dt.days # 读一本书的耗时
fig2 = px.histogram(df, x='read period')
st.plotly_chart(fig2)


# 6、每本书包含的页数范围
st.markdown("### 6. 每本书包含的页数范围")
fig3 = px.histogram(df,
                    x = 'Number of Pages',
                    title = '每本书的页数')
st.plotly_chart(fig3)


# 7、图书出版日期分布
st.markdown("### 7. 图书出版日期分布")
books_publication_year = df.groupby('Original Publication Year')['Book Id'].count().reset_index() # 分组
books_publication_year.columns = ['year published', 'count'] # 列名重置
fig4 = px.bar(books_publication_year,
              x = 'year published',
              y = 'count',
              title = 'Book Published Year')
fig4.update_xaxes(range=[1850, 2021]) # 横坐标范围设置
st.plotly_chart(fig4)


# 8、图书评分分布
st.markdown("### 8. 图书评分分布")
df = df[df['My Rating'] != 0]
# 个人用户评分
fig5 = px.histogram(df,
                    x = 'My Rating',
                    title = "User Rating")
st.plotly_chart(fig5)

# 9、平均用户评分
st.markdown("### 9. 平均用户评分")
fig6 = px.histogram(df,
                    x = 'Average Rating',
                    title = 'Average Rating')
st.plotly_chart(fig6)
