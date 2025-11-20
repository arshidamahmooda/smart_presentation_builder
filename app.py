import streamlit as st
from models.text_summarizer import summarize_text
from models.ppt_generator import generate_presentation

st.set_page_config(page_title="Smart Presentation Builder", page_icon="📊")

st.title("📊 Smart Presentation Builder (Offline - No API Needed)")

st.write("📝 Paste your text below to generate a presentation automatically!")

user_input = st.text_area("Enter your document text here", height=300)

if st.button("Generate Presentation"):
    if not user_input.strip():
        st.warning("⚠️ Please enter some text!")
    else:
        with st.spinner("⏳ Summarizing text..."):
            summary_points = summarize_text(user_input)

        st.success("✔️ Summary created!")

        with st.spinner("🎨 Generating PPTX file..."):
            ppt_file = generate_presentation(summary_points)

        st.success("🎉 Presentation Ready!")

        st.download_button(
            label="⬇️ Download Presentation",
            data=ppt_file,
            file_name="presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
