import streamlit as st
from textblob import TextBlob
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import re

nltk.download('wordnet')

'''
参考API链接：
1. textblob : https://textblob.readthedocs.io/en/dev/
2. NLTK : https://www.nltk.org/
'''

def main():
    # 用户输入
    st.title("NLP app: 情感分析案例")
    st.subheader("欢迎使用我们的APP功能")
    text = st.text_input(label="请输入文本内容")

    # 文本清理
    text = re.sub(r"[^A-Za-z0-9]"," ", text) # 仅保留字母和数字

    # 文本split
    text = text.split()
    # 词形还原
    lm = WordNetLemmatizer()
    lemmatized_words = [lm.lemmatize(word) for word in text]
    # 重新拼接
    text = ' '.join(lemmatized_words)

    # 预测
    if st.button("开始分析"):
        blob = TextBlob(text)
        result = blob.sentiment.polarity # 极性分数

        if result > 0.0:
            custom_emoji = ':blush:'
            st.success('开心 : {}'.format(custom_emoji))
        elif result < 0.0:
            custom_emoji = ':disappointed:'
            st.warning('悲伤 : {}'.format(custom_emoji))
        else:
            custom_emoji = ':confused:'
            st.info('中立 : {}'.format(custom_emoji))

        st.success('分数 = {}'.format(result))


if __name__ == "__main__":
    main()
