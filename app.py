import streamlit as st
from pptx import Presentation
from io import BytesIO
import json
from transformers import pipeline

# ---------------- LLM (No API Required) ----------------
generator = pipeline("text2text-generation", model="google/flan-t5-large")

st.set_page_config(page_title="Free AI Smart Presentation Builder", layout="centered")
st.title("🎯 Smart Presentation Builder (FREE - No API Key)")
st.write("Generate PPT slides using open-source AI 🤖✨")

# ---------------- Slide Creation ----------------
def generate_slides(topic, num_slides):
    prompt = f"""
    Create {num_slides} slides about {topic}.
    Return output in STRICT JSON list format:
    [
      {{"title":"Slide Title","bullets":["short point1","short point2"]}}
    ]
    Use simple bullet points.
    """

    response = generator(prompt, max_length=500)[0]["generated_text"]
    
    # Fix accidental formatting
    response = response.replace("```json", "").replace("```", "")
    try:
        slides = json.loads(response)
    except:
        # fallback if output is not valid JSON 
        slides = [
            {
                "title": f"{topic} - Slide {i+1}",
                "bullets": [f"Point {j+1}" for j in range(3)]
            }
            for i in range(num_slides)
        ]
    return slides


# ---------------- Create PPTX ----------------
def create_ppt(slides, topic):
    prs = Presentation()

    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = topic

    for s in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = s["title"]
        tf = slide.shapes.placeholders[1].text_frame
        tf.clear()

        for i, bullet in enumerate(s["bullets"]):
            if i == 0:
                tf.text = bullet
            else:
                p = tf.add_paragraph()
                p.text = bullet

    ppt_data = BytesIO()
    prs.save(ppt_data)
    ppt_data.seek(0)
    return ppt_data


# ---------------- UI Controls ----------------
topic = st.text_input("Enter your topic 📝")
num_slides = st.slider("Number of Slides", 3, 10, 5)

if st.button("Generate Presentation 🚀"):
    if not topic:
        st.error("Please enter a topic!")
    else:
        with st.spinner("Generating content... ⏳"):
            slides = generate_slides(topic, num_slides)
            ppt = create_ppt(slides, topic)

            st.success("🎉 PPT Ready!")

            st.download_button(
                label="📥 Download PPT",
                data=ppt,
                file_name=topic.replace(" ", "_") + ".pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

            st.subheader("👀 Slide Preview")
            for i, s in enumerate(slides):
                st.write(f"### Slide {i+1}: {s['title']}")
                for bullet in s["bullets"]:
                    st.write("- " + bullet)
