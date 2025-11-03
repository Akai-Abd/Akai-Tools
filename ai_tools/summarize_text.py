"""
Summarize any text file using OpenAI or local models.
Usage:
    python summarize_text.py input.txt
"""
import sys
import openai  # pip install openai

openai.api_key = "your_api_key_here"  # replace or use environment variable

def summarize_text(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize text concisely."},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message["content"].strip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarize_text.py input.txt")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
    print("\n🧠 Summary:\n")
    print(summarize_text(text))
