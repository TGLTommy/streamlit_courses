import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# 加载模型
with st.spinner("加载模型中..."):
    model = tf.keras.models.load_model("02-Projects/p-01-animal_app/model/animal.hdf5")

# 用户上传图片
upload_file = st.file_uploader("请选择一张图片上传", type=['jpg','png'])

# 动物类别标签定义
animal_labels = {
    0: '狗',
    1: '马',
    2: '大象',
    3: '蝴蝶',
    4: '鸡',
    5: '猫',
    6: '牛'
}

# 图片预处理，然后输入到模型进行预测
if upload_file is not None:
    image = np.array(bytearray(upload_file.read()), dtype='uint8') # 读取图片
    image = cv2.imdecode(image, cv2.IMREAD_COLOR) # 字节解码
    RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # 图片通道转换
    img_resize = cv2.resize(RGB_img, (224,224)) # 图片尺寸转换，用于模型输入
    # 显示图片
    st.markdown("### 用户上传图片，显示如下: ")
    st.image(RGB_img, channels="RGB")
    # mobilenet预处理图片
    img_resize = preprocess_input(img_resize) # (224, 224, 3)
    #print("img_size: ", img_resize.shape)
    # 增加一个维度
    img_reshape = img_resize[np.newaxis, ...] # (1, 224, 224, 3)
    #print("img_reshape: ", img_reshape.shape)
    # 模型预测
    st.markdown("**请点击按钮开始预测**")
    predict = st.button("类别预测")
    if predict:
        prediction = model.predict(img_reshape)
        #print("prediction : ", prediction)
        max_pred_position = prediction.argmax() # 最大值的索引
        st.title("图片中的动物类别是: {}".format(animal_labels[max_pred_position]))

