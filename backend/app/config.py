import os
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    app_name: str = "AI PR Reviewer"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    github_app_id: str = os.getenv("GITHUB_APP_ID", "")
    github_private_key: str = os.getenv("GITHUB_PRIVATE_KEY", "")
    github_webhook_secret: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    base_url: str = os.getenv("BASE_URL", "http://localhost:8000")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    review_history_size: int = int(os.getenv("REVIEW_HISTORY_SIZE", "50"))
    max_files: int = int(os.getenv("MAX_REVIEW_FILES", "20"))
    max_patch_chars: int = int(os.getenv("MAX_PATCH_CHARS", "20000"))
    llm_timeout_seconds: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "30"))
    allow_stub_reviews: bool = os.getenv("ALLOW_STUB_REVIEWS", "true").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


settings = Settings()
