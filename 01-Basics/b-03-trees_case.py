
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 1、设置页面
st.set_page_config(
    page_title="streamlit tree app",
    layout="wide"
)
st.title("Trees Case")
df = pd.read_csv("01-Basics/data/trees.csv")

# 2、侧边栏：根据字段caretaker过滤数据
owners = st.sidebar.multiselect(
    "Tree owner filter : ",
    df['caretaker'].unique()
)
st.write("当前树的拥有者是：{}".format(owners))
if owners:
    # 根据选择caretaker进行过滤
    df = df[df['caretaker'].isin(owners)]

# 侧边栏：颜色选择（显示图示时，可以自定颜色）
graph_color = st.sidebar.color_picker('Graph Colors')

# 3、数据可视化
st.markdown("### 默认显示前5行")
st.write("df shape : ", df.shape)
st.write(df.head())
st.markdown("### 根据字段dbh分组统计")
df_groupby_dbh_count = pd.DataFrame(df.groupby(['dbh']).count()['tree_id'].sort_values(ascending=False))
df_groupby_dbh_count.columns = ['tree_count'] # 修改列名
st.write(df_groupby_dbh_count)

# 4、三列显示
# 方式1：设置表格属性，每一列的宽度相等
# col_1, col_2, col_3 = st.columns(3)

# 方式2：设置表格属性，根据用户输入，自定义每一列的宽度
first_width = st.number_input(
    label = "第一列宽度: ",
    min_value = 1,
    max_value = 20,
    value = 1
)

second_width = st.number_input(
    label = "第二列宽度: ",
    min_value = 1,
    max_value = 20,
    value = 1
)

third_width = st.number_input(
    label = "第三列宽度: ",
    min_value = 1,
    max_value = 20,
    value = 1
)

col_1, col_2, col_3 = st.columns((first_width, second_width, third_width))

with col_1:
    st.header("列-1")
    st.line_chart(df_groupby_dbh_count)
    st.subheader("根据经纬度，显示地图")
    # 清理'经度'和'维度'中的NaN
    new_df = df.dropna(subset=['longitude', 'latitude'])
    # 随机选择500个样本
    new_df = new_df.sample(n=500)
    # st.map
    st.map(new_df)

with col_2:
    st.header("列-2")
    st.bar_chart(df_groupby_dbh_count)
    # 新建一个字段 age，并显示
    df['age_days'] = (pd.to_datetime('2023-01-14') - pd.to_datetime(df['date'])).dt.days
    st.subheader("histplot about age")
    fig_1, ax_1 = plt.subplots()
    ax_1 = sns.histplot(df['age_days'], color=graph_color)
    plt.xlabel('Age (Days)')
    plt.title("Tree Age")
    st.pyplot(fig_1)

with col_3:
    st.header("列-3")
    st.area_chart(df_groupby_dbh_count)
    st.subheader("histplot about Tree Width")
    fig_2, ax_2 = plt.subplots()
    ax_2 = sns.histplot(df['dbh'], color=graph_color)
    plt.xlabel("Tree width")
    plt.title("Tree Width")
    st.pyplot(fig_2)


