"""Version: v0.1
1. 加载模型
2. 根据用户输入数据，进行预测
"""
import streamlit as st
import pickle

# 设置 title
st.title("*** 企鹅(Penguin)分类案例 ***")

# 加载模型
with open("rfc_model.pickle", "rb") as file:
    rfc_model = pickle.load(file)
    st.write("### rfc model : \n", rfc_model)

# 加载标签名称
with open("label_names.pickle", "rb") as file:
    label_names = pickle.load(file)
    st.write("### label names : \n", label_names)

# 模型预测
# 用户输入特征数据：

# island
island = st.selectbox(
    label = "企鹅所在的岛屿: ",
    options = ['Biscoe', 'Dream', 'Torgerson']
)

# sex
sex = st.selectbox(
    label = "企鹅的性别: ",
    options = ['Female', 'Male']
)

with st.form(key="penguin"):
    # bill_length, bill_depth, flipper_length, body_mass
    bill_length = st.slider("Bill Length (mm)", 20, 60, 40)

    bill_depth = st.slider("Bill Depth (mm) ", 10, 40, 25)

    flipper_length = st.slider("Flipper Length (mm) ", 170, 240, 200)

    body_mass = st.slider("Body Mass (g) ", 2900, 5000, 3500)

    st.write("### 用户输入的特征数据：{}".format([island, sex, bill_depth, bill_length, flipper_length, body_mass]))

    submitted = st.form_submit_button("提交: 开始预测企业类别")

    if submitted:
        # 将 island 和 sex 转换 one-hot
        island_Biscoe, island_Dream, island_Torgersen = 0, 0, 0
        if island == 'Biscoe':
            island_Biscoe = 1
        elif island == 'Dream':
            island_Dream = 1
        elif island == 'Torgerson':
            island_Torgersen = 1

        sex_female, sex_male = 0, 0
        if sex == 'Female':
            sex_female = 1
        elif sex == 'Male':
            sex_male = 1

        # 将所有特征合并起来
        temp_feature = [bill_length, bill_depth, flipper_length, body_mass, island_Biscoe, island_Dream, island_Torgersen,
                        sex_female, sex_male]

        # 模型预测
        new_prediction = rfc_model.predict([temp_feature])

        # 预测的企鹅类别
        predict_species = label_names[new_prediction][0]

        st.write("### 模型的预测类别: ", predict_species)

