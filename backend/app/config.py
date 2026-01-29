from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = "AI PR Reviewer"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    github_app_id: str = os.getenv("GITHUB_APP_ID", "")
    github_private_key: str = os.getenv("GITHUB_PRIVATE_KEY", "")
    github_webhook_secret: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    base_url: str = os.getenv("BASE_URL", "http://localhost:8000")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")


settings = Settings()
