import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc("font", family='AR PL UMing CN')

# 1. st.write()
st.write("1. st.write()")
st.write(pd.DataFrame({
    '第一列': [1,2,3,4],
    '第二列': [10,20,30,40]}
))

# 2. st.line_chart()
st.write("2. st.line_chart()")
chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=['a','b','c']
)
st.line_chart(chart_data)

# 3. st.map()
st.write("3. st.map()")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50,50] + [37.76,-122.4],
    columns=['lat', 'lon']
)
st.map(map_data)

# 4. st.slider()
st.write("4. st.slider()")
x = st.slider("x")
st.write(x, "squred is", x*x)

# 5. st.text_input()
st.write("5. st.text_input()")
st.text_input("your name", key="name")
# 显示输入的值
st.session_state.name

# 6. st.checkbox() 多选框
st.write("6. st.checkbox()")
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20,3),
        columns=['a','b','c']
    )
    chart_data


# 7. st.selectbox() 下拉选项
st.write("7. st.selectbox()")
df = pd.DataFrame({
    '第1列': [1,2,3,4]
})

option = st.selectbox(
    'which number do you like best?',
    df['第1列']
)

"you selected: ", option


# 8. st.sidebar 侧边栏
st.write("8. st.sidebar")
add_selectbox = st.sidebar.selectbox(
    "通讯方式选项",
    ('微信','QQ','手机','邮件')
)
"下拉选项: ", add_selectbox

add_slider = st.sidebar.slider(
    "选择一个范围的值",
    0.0, 100.0, (25.0, 75.0)
)
"值的范围: ", add_slider

# 9. st.radio() 单选
st.write("10. st.radio()")
left_column, right_column = st.columns(2)
# 左边列设置
left_column.button("Press me!")
# 右边列设置
with right_column:
    chosen = st.radio(
        '手机品牌',
        ('苹果','华为','小米','三星')
    )
    st.write(f'你选择的品牌是: {chosen}')

# 10. st.progress() 进度条
st.write("10. st.progress()")
import time
st.write("模拟长时间的计算...")
# 添加placeholder
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    # 更新进度条
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.1)
'运行结束!'


# 11. st.file_uploader() 上传文件
st.write("11. st.file_uploader()")
upload_file = st.file_uploader(
    label = "上传数据集CSV文件"
)

if upload_file is not None:
    # 不为空
    df = pd.read_csv(upload_file)
    st.success("上传文件成功！")
else:
    st.stop() # 退出

# 选择横坐标和纵坐标属性
x_var = st.selectbox(
    label = "选择横坐标的属性",
    options = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
)

y_var = st.selectbox(
    label = "选择纵坐标的属性",
    options = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
)

sns.set_style("darkgrid")
markers = {'Adelie':'s',
           'Gentoo':'X',
           'Chinstrap':'o'}

fig, ax = plt.subplots()
ax = sns.scatterplot(data=df,
                     x=x_var,
                     y=y_var,
                     hue='species',
                     markers=markers,
                     style='species')
plt.xlabel(x_var)
plt.ylabel(y_var)
plt.title('Penguins Scatter Plot')
st.pyplot(fig)

