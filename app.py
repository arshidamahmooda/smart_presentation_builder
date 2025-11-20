import streamlit as st
import requests
from pptx import Presentation
from io import BytesIO
import json

st.set_page_config(page_title="Smart Presentation Builder", layout="centered")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

st.title("🎯 Smart Presentation Builder (FREE - HuggingFace API)")
st.write("Generate PowerPoint slides using a lightweight, fast Generative AI model.")

hf_token = st.sidebar.text_input("Hugging Face API Token 🗝", type="password")
num_slides = st.sidebar.slider("Number of Slides", 3, 12, 6)
topic = st.text_input("Enter Topic")

headers = {}

if hf_token:
    headers = {"Authorization": f"Bearer {hf_token}"}

def generate_slides(topic, n):
    prompt = f"""
    Create {n} PowerPoint slides on "{topic}".
    Return pure JSON list only:
    [
      {{"title":"Slide title","bullets":["short text","short text"]}}
    ]
    Keep bullets <= 10 words.
    """
    data = {"inputs": prompt, "max_new_tokens": 500}
    response = requests.post(API_URL, headers=headers, json=data)

    result = response.json()[0]["generated_text"]
    result = result.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(result)
    except:
        raise ValueError("Model returned invalid JSON. Try again.")

def create_ppt(slides, topic):
    prs = Presentation()

    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = topic

    for s in slides:
        sl = prs.slides.add_slide(prs.slide_layouts[1])
        sl.shapes.title.text = s["title"]
        tf = sl.shapes.placeholders[1].text_frame
        tf.clear()
        for i, b in enumerate(s["bullets"]):
            if i == 0:
                tf.text = b
            else:
                p = tf.add_paragraph()
                p.text = b

    bio = BytesIO()
    prs.save(bio)
    bio.seek(0)
    return bio


if st.button("Generate PPT"):
    if not hf_token:
        st.error("⚠️ Enter HuggingFace API Token in sidebar!")
    elif topic == "":
        st.warning("Enter a topic.")
    else:
        with st.spinner("⏳ Generating slides..."):
            try:
                slides = generate_slides(topic, num_slides)
                ppt = create_ppt(slides, topic)
                filename = topic.replace(" ", "_") + ".pptx"
                st.success("🎉 Slides generated!")
                st.download_button("📥 Download PPT", data=ppt,
                                   file_name=filename,
                                   mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
                st.subheader("👀 Preview")
                for i, s in enumerate(slides):
                    st.markdown(f"### Slide {i+1}: {s['title']}")
                    for b in s["bullets"]:
                        st.write(f"- {b}")

            except Exception as e:
                st.error(f"❌ Error: {e}")
