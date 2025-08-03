import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

st.set_page_config(page_title="📝 أداة تحليل النصوص", layout="centered")
st.title("📝 أداة تحليل النصوص")

text_input = st.text_area("📥 أدخل النص المراد تحليله", height=300)

if st.button("🔍 تحليل"):
    if text_input.strip() == "":
        st.warning("يرجى إدخال نص لتحليله.")
    else:
        # تنظيف النص من الرموز
        clean_text = re.sub(r"[^\w\s]", "", text_input)
        words = clean_text.split()
        word_counts = Counter(words)

        # عرض أكثر الكلمات تكرارًا
        st.subheader("📌 أكثر الكلمات تكرارًا")
        for word, count in word_counts.most_common(10):
            st.write(f"🔹 {word} — {count} مرة")

        # توليد سحابة كلمات
        st.subheader("☁️ سحابة الكلمات")
        wordcloud = WordCloud(
            font_path="arial",  # استخدم مسار خط يدعم العربية إذا توفر
            width=800,
            height=400,
            background_color="white"
        ).generate(" ".join(words))

        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
