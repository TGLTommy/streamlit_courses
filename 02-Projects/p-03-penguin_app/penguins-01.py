import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# 设置中文字体显示
matplotlib.rc("font", family='AR PL UMing CN')
st.title("Penguins Example") # 标题
st.markdown("*** 读取数据后，进行可视化展示 ***") # 注释


### 1、上传文件 或 默认文件
# st.file_uploader 上传文件

uploaded_file = st.file_uploader(
    label = "选择本地的CSV文件"
)

# 将数据进行缓存
@st.cache()
def load_file(file):
    if file is not None:
        # 如果上传文件存在
        df = pd.read_csv(file)
        return df
    else:
        # 如果没有上传文件或失败，加载默认的文件
        #df = pd.read_csv("penguins.csv")
        # 如果不需要默认显示，则stop
        st.stop()

# 调用方法
df = load_file(uploaded_file)

copy_df = df.copy()

# 显示前5行数据
st.markdown("*** 显示数据集的默认前5行 ***")
st.write(df.head())


### 2、针对单个种类企鹅进行筛选，可视化显示
st.write("*** 单个企鹅种类可视化 ***")
# ① 企鹅种类
species = st.selectbox(
    label = "请选择需要显示的企业类别: ",
    options = ('Adelie', 'Gentoo', 'Chinstrap'),
    key = 1
)
df = df[df['species'] == species] # 根据选择类别筛选

# ② x 横坐标
x_axis = st.selectbox(
    label = "请选择横坐标",
    options = ('bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'),
    key = 2
)
# ③ y 纵坐标
y_axis = st.selectbox(
    label = "请选择纵坐标",
    options = ('bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'),
    key = 3
)
# ④ 根据企鹅性别选择
gender = st.selectbox(
    label = "选择企鹅的性别: ",
    options = ('all penguins', 'male penguins', 'female penguins'),
    key = 4
)

if gender == 'male penguins':
    df = df[df['sex']=='male']
elif gender == 'female penguins':
    df = df[df['sex']=='female']
else:
    pass

# 根据 species 筛选数据
fig, ax = plt.subplots()
ax = sns.scatterplot(x = df[x_axis],
                     y = df[y_axis])
plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.title('{}企鹅, 性别: {}'.format(species, gender))
st.pyplot(fig)  # st.pyplot()




### 3、多个种类一起显示
st.write("*** 多个类别的企鹅可视化 ***")
# x 横坐标
x_axis_2 = st.selectbox(
    label = "请选择横坐标",
    options = ('bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g')
)
# y 纵坐标
y_axis_2 = st.selectbox(
    label = "请选择纵坐标",
    options = ('bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g')
)
# 根据企鹅性别选择
gender_2 = st.selectbox(
    label = "选择企鹅的性别: ",
    options = ('all penguins', 'male penguins', 'female penguins')
)

if gender_2 == 'male penguins':
    df = df[df['sex']=='male']
elif gender_2 == 'female penguins':
    df = df[df['sex']=='female']
else:
    pass

# 根据 species 筛选数据
sns.set_style("darkgrid")
markers = {"Adelie":"X",
           "Gentoo":"s",
           "Chinstrap":"o"}
fig, ax = plt.subplots()
ax = sns.scatterplot(data = copy_df,
                     x = x_axis_2,
                     y = y_axis_2,
                     hue = 'species',
                     markers=markers,
                     style='species')
plt.xlabel(x_axis_2)
plt.ylabel(y_axis_2)
plt.title('{} scatterplot'.format(species))
st.pyplot(fig)






