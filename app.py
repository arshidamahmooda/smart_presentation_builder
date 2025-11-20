import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

import streamlit as st
from ppt_generator import generate_presentation_green_theme
from text_summarizer import split_into_slides

st.set_page_config(page_title="Smart Presentation Builder", page_icon="💡")

st.title("🧠 Smart AI Presentation Builder (Offline)")
st.write("Paste content → Auto-generate a clean professional PPT! 💼")

content = st.text_area("✍️ Enter content for slides:", height=350,
                       placeholder="Paste your slide content here...")

slide_count = st.slider("📌 Number of slides", 3, 12, 6)

if st.button("✨ Generate Presentation"):
    if content.strip() == "":
        st.error("⚠ Please enter presentation content!")
    else:
        with st.spinner("💡 Structuring slides..."):
            slides = split_into_slides(content, slide_count)

        with st.spinner("🎨 Designing presentation with icons..."):
            ppt = generate_presentation_green_theme(slides)

        st.success("🎉 PPT Successfully Generated!")
        st.download_button(
            "📥 Download Presentation",
            data=ppt,
            file_name="Smart_AI_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

        st.subheader("📌 Slide Preview")
        for i, slide in enumerate(slides):
            st.markdown(f"### Slide {i+1}: {slide['title']}")
            for bullet in slide['bullets']:
                st.write(f"- {bullet}")
