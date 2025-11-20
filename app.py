import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

import streamlit as st
from text_summarizer import summarize_text
from ppt_generator import generate_presentation

st.set_page_config(page_title="Smart Presentation Builder", page_icon="📊")

st.title("📊 Smart Presentation Builder (Offline - No API Needed)")
st.write("Enter your topic/content — Download your PPT instantly 🚀")

user_input = st.text_area("📝 Enter content for slides:", height=300)
slide_count = st.slider("Select number of slides", 3, 12, 6)

if st.button("Generate Presentation"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text!")
    else:
        with st.spinner("✍️ Creating presentation…"):
            bullet_points = summarize_text(user_input, slide_count)
            ppt_file = generate_presentation(bullet_points)

            st.success("🎉 Presentation Ready!")
            st.download_button(
                label="📥 Download PPT",
                data=ppt_file,
                file_name="ai_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
