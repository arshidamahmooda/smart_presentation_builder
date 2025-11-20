import streamlit as st
import google.generativeai as genai
from pptx import Presentation
from io import BytesIO
import json

# ---------------- CONFIG ----------------
API_KEY = "AIzaSyAJjoVkoZ8mLwIX9gBLrDyKoHxbHsCj6A8"
 # 🔑 Replace with your Gemini API key
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Smart Presentation Builder", layout="centered")

# ---------------- LLM SLIDE CREATION ----------------
def generate_slides(topic, num_slides):
    prompt = f"""
    Create {num_slides} PowerPoint slides on the topic: "{topic}".
    Output must be a valid JSON list only.
    Format:
    [
      {{"title": "Slide Title", "bullets": ["short bullet 1", "short bullet 2"]}}
    ]
    Each bullet must be less than 12 words.
    Do not include extra text other than the pure JSON list.
    """

    # … inside generate_slides …
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)


    slides_json = response.text.strip()
    slides_json = slides_json.replace("```json", "").replace("```", "")
    return json.loads(slides_json)

# ---------------- PPTX BUILDER ----------------
def create_ppt(slides, topic):
    prs = Presentation()

    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = topic

    # Slides creation
    for s in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = s["title"]

        text_frame = slide.shapes.placeholders[1].text_frame
        text_frame.clear()

        for i, bullet in enumerate(s["bullets"]):
            if i == 0:
                text_frame.text = bullet
            else:
                p = text_frame.add_paragraph()
                p.text = bullet

    ppt_data = BytesIO()
    prs.save(ppt_data)
    ppt_data.seek(0)
    return ppt_data


# ---------------- STREAMLIT UI ----------------
st.title("🎯 Smart Presentation Builder - Powered by Gemini AI")
st.write("Generate professional PPT slides instantly using Generative AI! 🚀")

topic = st.text_input("Topic for Presentation 📝")
num_slides = st.slider("Select Number of Slides", 3, 12, 6)

if st.button("Generate Presentation ✨"):
    if "YOUR_GEMINI_API_KEY" in API_KEY:
        st.error("⚠️ Please update your Gemini API key in the code!")
    elif topic == "":
        st.warning("Please enter a topic!")
    else:
        with st.spinner("Generating Slides... ⏳"):
            try:
                slides = generate_slides(topic, num_slides)
                ppt_file = create_ppt(slides, topic)

                file_name = topic.replace(" ", "_")[:40] + ".pptx"

                st.success("🎉 Done! Your PPT is ready.")
                st.download_button(
                    label="📥 Download PPT",
                    data=ppt_file,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )

                st.subheader("👀 Slide Preview")
                for i, s in enumerate(slides):
                    st.markdown(f"### Slide {i+1}: {s['title']}")
                    for b in s["bullets"]:
                        st.write(f"- {b}")

            except Exception as e:
                st.error(f"❌ Error: {e}")
