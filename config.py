import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")
# LangChain settings
TEMPERATURE = 0.7
MAX_TOKENS = 1024
