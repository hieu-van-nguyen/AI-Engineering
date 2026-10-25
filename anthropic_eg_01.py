import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
baseUrl = os.getenv("ANTHROPIC_BASE_URL")
apiKey = os.getenv("ANTHROPIC_API_KEY")
authToken = os.getenv("ANTHROPIC_AUTH_TOKEN")
model = os.getenv("ANTHROPIC_MODEL")

client = anthropic.Anthropic(
    base_url=baseUrl,
    api_key=apiKey,  # required but ignored
)

message = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=[{'role': 'user', 'content': 'Write a function to check if a number is prime'}]
)

print(message.content[0].text)