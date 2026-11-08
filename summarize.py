"""Day 4: send ONE paper to Gemini and get a plain-English summary back.

Run:  python summarize.py        (summarizes the newest paper)
      python summarize.py 5      (summarizes paper #5 from the radar list)
"""
import os
import sys

from dotenv import load_dotenv
from google import genai

from config import GEMINI_MODEL
from radar import collect_papers

# The prompt is the instructions we give the model. Changing this text changes
# what you get back, so experiment with it. {title} and {abstract} get filled in.
PROMPT = """You are helping a high school student keep up with AI x biology research.
Summarize this paper in exactly 3 short sentences, in plain English (no jargon,
or explain any jargon you must use):

1. What they did.
2. Why it matters.
3. One sharp question you would ask the authors in an interview.

Title: {title}

Abstract: {abstract}"""


def make_client():
    """Load the API key from .env and create a Gemini client."""
    load_dotenv()  # reads the .env file and puts GEMINI_API_KEY into the environment
    if not os.getenv("GEMINI_API_KEY"):
        sys.exit("No GEMINI_API_KEY found. Create a file called .env with:\n"
                 "GEMINI_API_KEY=your-key-here")
    return genai.Client()  # automatically picks up GEMINI_API_KEY


def summarize(client, paper):
    """Send one paper to the model and return its summary text."""
    prompt = PROMPT.format(title=paper["title"], abstract=paper["abstract"])
    interaction = client.interactions.create(model=GEMINI_MODEL, input=prompt)
    return interaction.output_text


def main():
    client = make_client()
    papers = collect_papers()
    if not papers:
        sys.exit("No papers found. Try raising DAYS_BACK in config.py.")

    # Which paper? Default is #1 (newest). `python summarize.py 5` picks #5.
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    paper = papers[n - 1]

    print(f"\n{paper['title']}")
    print(f"{paper['source']} · {paper['date']} · {paper['url']}\n")
    print("Asking Gemini...\n")
    print(summarize(client, paper))


if __name__ == "__main__":
    main()
