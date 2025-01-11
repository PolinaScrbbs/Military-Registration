import os
from dotenv import load_dotenv

os.environ.pop("API_URL", None)

load_dotenv()

API_URL = os.getenv("API_URL")
