import os
from dotenv import load_dotenv

os.environ.pop("API_URL", None)
os.environ.pop("API_SECRET_KEY", None)
os.environ.pop("SECRET_KEY", None)

load_dotenv()

API_URL = os.getenv("API_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
