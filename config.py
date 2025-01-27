import os
from dotenv import load_dotenv

os.environ.pop("ENV", None)

os.environ.pop("HOST", None)
os.environ.pop("PORT", None)

os.environ.pop("DBNAME", None)
os.environ.pop("USER", None)
os.environ.pop("PASSWORD", None)

os.environ.pop("SECRET_KEY", None)
os.environ.pop("TOKEN_LIFETIME", None)

os.environ.pop("MEDIA_ROOT", None)


class Config:
    def __init__(self):
        load_dotenv()

        self.env = os.getenv("ENV")

        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.db_name = os.getenv("DBNAME")

        self.secret_key = os.getenv("SECRET_KEY")
        self.token_lifetime = int(os.getenv("TOKEN_LIFETIME"))

        self.media_root = os.getenv("MEDIA_ROOT")

        self.database_url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


config = Config()
