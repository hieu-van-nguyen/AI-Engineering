import os
from dotenv import load_dotenv
load_dotenv()
print({k: bool(os.getenv(k)) for k in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]})