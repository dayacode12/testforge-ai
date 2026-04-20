import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
TESTFORGE_URL = os.getenv("TESTFORGE_URL")
APP_ENV = os.getenv("APP_ENV")
DEBUG = os.getenv("DEBUG") == "true"