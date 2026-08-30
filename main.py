import os
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# تنظیمات اولیه صفحه استریم‌لیت
st.set_page_config(page_title="Executive News Intelligence", layout="wide")

# خواندن امن کلید API از متغیرهای محیطی یا Streamlit Secrets
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    genai.configure(api_key=api_key)

st.title("📰 سامانه پایش و تحلیل هوشمند اخبار")

# کادر دریافت ورودی اخبار خام
raw_input = st.text_area("اخبار خام را در این قسمت وارد کنید:", height=250)

if st.button("تولید بولتن خبری"):
    if not api_key:
        st.error("کلید API یافت نشد! پس از دپلوی، آن را در بخش Secrets استریم‌لیت وارد کنید.")
    elif not raw_input.strip():
        st.warning("لطفاً ابتدا متنی را وارد کنید.")
    else:
        with st.spinner("در حال پردازش و خلاصه‌سازی با جمینای..."):
            try:
                prompt = f"""
You are an executive media monitoring specialist. Process the raw news below into a structured news bulletin.

STRICT ENTRY STRUCTURE REQUIREMENT:
For EVERY individual news article selected, display it clearly with source, summary, and context.

RAW DATA:
{raw_input}
"""
               model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(prompt)
                
                st.subheader("📋 بولتن خروجی:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"خطا در پردازش: {e}")
