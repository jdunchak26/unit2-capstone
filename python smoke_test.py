# smoke_test.py
# confirming that google gemini is reachable
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), 
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
message = client.chat.completions.create(
    model="gemini-3.5-flash-lite",
    max_tokens=500,
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)


print(message.choices[0].message.content)
print(f"Input tokens: {message.usage.prompt_tokens}")
print(f"Output tokens: {message.usage.completion_tokens}")

