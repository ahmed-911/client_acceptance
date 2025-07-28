import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="تحليل معدلات الرضى", layout="centered")
st.title("📊 تحليل معدلات الرضى من ملف Excel")

uploaded_file = st.file_uploader("⬆️ قم برفع ملف Excel بصيغة .xlsx", type=["xlsx", "xls"])

# دالة إزالة التشكيل من النص
def remove_diacritics(text):
    arabic_diacritics = re.compile(r'[\u064B-\u0652]')
    return re.sub(arabic_diacritics, '', str(text)).strip()

# قاموس ترميز الإجابات بدون تشكيل
mapping = {
    'راض تماما': 5,
    'راض': 4,
    'محايد': 3,
    'غير راض': 2,
    'غير راض تماما': 1
}

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("🧾 الأعمدة الموجودة في الملف:")
    st.write(df.columns.tolist())

    selected_columns = st.multiselect("🔍 اختر الأعمدة التي تريد تحليل معدل الرضا لها", df.columns)

    if selected_columns:
        for col in selected_columns:
            # تنظيف النصوص من التشكيل قبل الترميز
            cleaned_col = col + '_clean'
            df[cleaned_col] = df[col].apply(remove_diacritics)
            df[col + '_num'] = df[cleaned_col].map(mapping)

        numeric_cols = [col + '_num' for col in selected_columns]
        df_clean = df.dropna(subset=numeric_cols)

        st.subheader("📈 نتائج التحليل:")
        results = {}
        for col in selected_columns:
            mean = df_clean[col + '_num'].mean()
            percent = (mean / 5) * 100
            results[col] = percent
            st.write(f"**{col}**: {mean:.2f} من 5 | نسبة الرضا: {percent:.1f}%")

        st.bar_chart(pd.Series(results, name="نسبة الرضا (%)"))
