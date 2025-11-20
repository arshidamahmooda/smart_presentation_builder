from transformers import pipeline

# Offline summarizer model
summarizer = pipeline("summarization", model="google/pegasus-xsum")

def summarize_text(text):
    summary = summarizer(text, max_length=60, min_length=30, do_sample=False)
    summary_text = summary[0]["summary_text"]

    # Convert summary into bullet points
    points = summary_text.split(". ")
    return [p.strip() for p in points if p.strip()]
