import streamlit as st
from openai import OpenAI
from pptx import Presentation
from io import BytesIO
import json

# ---------------- CONFIG ----------------
API_KEY = st.secrets["OPENAI_API_KEY"] # 🔑 Add your key
client = OpenAI(api_key=API_KEY)

st.set_page_config(page_title="Smart Presentation Builder", layout="centered")

# ---------------- LLM SLIDE CREATION ----------------
def generate_slides(topic, num_slides):
    prompt = f"""
    Create {num_slides} PowerPoint slides about the topic: {topic}.
    Output strictly a JSON list:
    [
      {{"title": "Slide Title", "bullets": ["short point 1", "short point 2"]}},
      ...
    ]
    Bullets must be short (under 12 words each).
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    slides_json = response.choices[0].message.content.strip()
    return json.loads(slides_json)

# ---------------- PPTX BUILDER ----------------
def create_pptx(slides, topic):
    prs = Presentation()
    
    # Title slide
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = topic
    
    # Slide Creation
    for s in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = s["title"]
        body = slide.shapes.placeholders[1].text_frame
        body.text = ""
        
        for i, bullet in enumerate(s["bullets"]):
            if i == 0:
                body.text = bullet
            else:
                p = body.add_paragraph()
                p.text = bullet

    ppt_data = BytesIO()
    prs.save(ppt_data)
    ppt_data.seek(0)
    return ppt_data

# ---------------- STREAMLIT UI ----------------
st.title("🎯 Smart Presentation Builder")
st.write("Generate professional PPT slides instantly using Generative AI!")

topic = st.text_input("Enter your presentation topic")
num_slides = st.slider("Number of Slides", 3, 12, 6)

if st.button("Generate Presentation 🧠✨"):
    if not API_KEY or "YOUR_API_KEY" in API_KEY:
        st.error("⚠️ Please provide a valid OpenAI API Key in the code before running")
    elif not topic:
        st.warning("Enter a topic to continue!")
    else:
        with st.spinner("⏳ Generating your presentation..."):
            try:
                slides = generate_slides(topic, num_slides)
                ppt = create_pptx(slides, topic)

                file_name = topic[:40].replace(" ", "_") + ".pptx"
                st.success("🎉 PPT Generated Successfully!")
                
                st.download_button(
                    label="📥 Download PPTX",
                    data=ppt,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
                
                st.subheader("📝 Slide Preview")
                for i, s in enumerate(slides):
                    st.write(f"**Slide {i+1}: {s['title']}**")
                    for b in s["bullets"]:
                        st.write("- " + b)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
