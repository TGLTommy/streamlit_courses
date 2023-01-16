import streamlit as st
import requests
import json

# 页面设置
st.set_page_config(page_title="语音到文本的转换",
                   page_icon="😄😄😄")

st.title("案例-02: 语音到文本的转换")

st.write("上传一个音频wav格式的文件，然后将解析的文本进行导出、保存")

# 设置三列
c1, c2, c3 = st.columns([1,4,1])

with c2:
    with st.form(key="my_form"):
        # 音频文件上传
        f = st.file_uploader("请上传音频wav格式的文件", type=[".wav"])
        # 表单提交
        submit_button = st.form_submit_button(label="开始转换")

    # 如果上传文件成功
    if f is not None:
        st.audio(f, format="wav") # 显示音频播放器
        # 文件名
        path_in = f.name
        st.write(f"file path: {path_in}")
        # 获取文件大小
        getsize = f.tell()
        getsize = round((getsize / 1000000), 1) # 计算文件大小，单位：MB

        if getsize < 5: # 如果文件小于5M
            # 按bytes读取
            bytes_value = f.getvalue()
            # 读取 huggingface 中的 token
            api_token = "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"
            # API key
            headers = {"Authorization": f"bearer {api_token}"}
            API_URL = ("https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h")

            def query(data):
                # 请求服务
                response = requests.request("POST",
                                            API_URL,
                                            headers=headers,
                                            data=data)
                return json.loads(response.content.decode("utf-8"))

            # 请求音频转文本服务
            data = query(bytes_value)

            # 获取结果
            result = data.values()
            text_value = next(iter(result)).lower()
            st.markdown("- **转换结果如下:**")
            st.info(text_value)

            # 下载转换后的文本
            st.download_button(
                "下载转换结果的文本",
                text_value,
                file_name="speech_to_text_result.txt"
            )
        else:
            st.warning(
                "警告⚠️: 上传文本大于5MB，请重新上传小一些的音频文件"
            )
    else:
        st.stop()




