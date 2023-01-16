"""Version: v0.2
1. 根据用户上传的训练数据进行模型训练
"""
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# 设置 title
st.title("### 企鹅(Penguin)分类案例 ###")

# 设置登录密码，如果用户输入正确，则进行后续代码运行
password_check = st.text_input("密码是什么?")
if password_check != st.secrets["password"]:
    st.stop()

# * 上传自定义的训练数据集
uploader_file = st.file_uploader(
    label = "Upload your own dataset"
)

input_df = None # 默认值

# * 如果上传成功，则按照之前的数据处理的流程走一遍；否则，直接调用之前的模型文件
if uploader_file is None:
    # 加载模型
    with open("02-Projects/p-03-penguin_app/rfc_model.pickle", "rb") as file:
        model = pickle.load(file)
        st.write("### rfc model : \n", model)
    # 加载标签名称
    with open("02-Projects/p-03-penguin_app/label_names.pickle", "rb") as file:
        label_names = pickle.load(file)
        st.write("### label names : \n", label_names)
else:
    input_df = pd.read_csv(uploader_file)
    input_df.dropna(inplace=True)
    labels = input_df['species'] # 标签
    targets, label_names = pd.factorize(labels) # 标签数值化
    features = input_df[input_df.columns[1:-1].values[:].tolist()] # 特征
    features_vector = pd.get_dummies(features) # one-hot
    # 数据集切分为：训练集 80% 和 测试集 20%
    x_train, x_test, y_train, y_test = train_test_split(features_vector, targets, test_size=0.2)
    # 模型：随机森林
    model = RandomForestClassifier(random_state=666)
    # 模型训练
    model.fit(x_train, y_train)
    # 模型预测
    y_pred = model.predict(x_test)
    # 计算 accuracy
    score = accuracy_score(y_pred, y_test)
    st.write("### 模型预测的得分: ", score)

    # 保存模型的重要性特征
    fig, ax = plt.subplots()
    st.markdown("模型特征重要性：")
    st.write(model.feature_importances_)
    ax = sns.barplot(x=model.feature_importances_, y=features_vector.columns)
    plt.title("模型的特征重要性")
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    fig.savefig('model_feature_importance.png')
    st.image("02-Projects/p-03-penguin_app/model_feature_importance.png")

# 模型预测
# 用户输入特征数据

# st.form 表单提交数据
with st.form('user_input'):
    # ① island
    island = st.selectbox(
        label = "企鹅所在的岛屿: ",
        options = ['Biscoe', 'Dream', 'Torgerson']
    )
    # ② sex
    sex = st.selectbox(
        label = "企鹅的性别: ",
        options = ['Female', 'Male']
    )
    # ③ bill_length
    bill_length = st.number_input(
        label = "Bill Length (mm) ",
        min_value = 0
    )
    # ④ bill_depth
    bill_depth = st.number_input(
        label = "Bill Depth (mm) ",
        min_value = 0
    )
    # ⑤ flipper_length
    flipper_length = st.number_input(
        label = "Flipper Length (mm) ",
        min_value = 0
    )
    # ⑥ body_mass
    body_mass = st.number_input(
        label = "Body Mass (g) ",
        min_value = 0
    )
    # 提交按钮
    submitted = st.form_submit_button('提交: 进行类别预测')
    if submitted:
        st.write("### 用户输入的特征数据：{}".format([island, sex, bill_depth, bill_length, flipper_length, body_mass]))
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
        new_prediction = model.predict([temp_feature])

        # 预测的企鹅类别
        predict_species = label_names[new_prediction][0]

        # 根据模型的特征重要性输出，绘制特征：bill length, bill depth, flipper length 的直方图
        st.subheader("预测的企鹅类别是：{}".format(predict_species))
