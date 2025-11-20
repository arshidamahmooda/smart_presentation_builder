from pptx import Presentation
from pptx.util import Pt
from io import BytesIO

icon = "🩺"

def generate_presentation_green_theme(slides):
    prs = Presentation()

    # Title Slide
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = slides[0]["title"]

    # Content Slides
    for slide_data in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = f"{icon} {slide_data['title']}"

        text_frame = slide.shapes.placeholders[1].text_frame
        text_frame.clear()

        for bullet in slide_data["bullets"]:
            p = text_frame.add_paragraph()
            p.text = f"• {bullet}"
            p.font.size = Pt(24)

    ppt_stream = BytesIO()
    prs.save(ppt_stream)
    ppt_stream.seek(0)
    return ppt_stream
