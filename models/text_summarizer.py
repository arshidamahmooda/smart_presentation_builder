import re

def split_into_slides(text, num_slides):
    blocks = re.split(r"\n\s*\n", text.strip())
    slides = []

    for block in blocks:
        lines = block.strip().split("\n")
        title = lines[0]
        bullets = lines[1:4]
        slides.append({"title": title, "bullets": bullets})

        if len(slides) >= num_slides:
            break

    return slides[:num_slides]
