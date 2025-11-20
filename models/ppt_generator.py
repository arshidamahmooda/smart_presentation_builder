from pptx import Presentation
from io import BytesIO

def generate_presentation(bullets):
    prs = Presentation()
    
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "AI Generated Presentation"

    for i, slide_bullets in enumerate(bullets):
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = f"Slide {i+1}"
        text_frame = slide.shapes.placeholders[1].text_frame
        text_frame.text = slide_bullets[0]
        
        for bullet in slide_bullets[1:]:
            p = text_frame.add_paragraph()
            p.text = bullet

    ppt_data = BytesIO()
    prs.save(ppt_data)
    ppt_data.seek(0)
    return ppt_data
