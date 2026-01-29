import hmac
import hashlib
from typing import List
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import PRInfo, ReviewResponse
from app.services.reviewer import analyze_pr
from app.services.github import fetch_pr

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REVIEWS: List[ReviewResponse] = []


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/review", response_model=ReviewResponse)
def review_pr(pr: PRInfo) -> ReviewResponse:
    review = analyze_pr(pr)
    REVIEWS.insert(0, review)
    return review


@app.post("/review/github", response_model=ReviewResponse)
def review_pr_from_github(
    repo_full_name: str,
    pr_number: int,
    access_token: str,
) -> ReviewResponse:
    pr = fetch_pr(access_token, repo_full_name, pr_number)
    review = analyze_pr(pr)
    REVIEWS.insert(0, review)
    return review


@app.get("/reviews", response_model=List[ReviewResponse])
def list_reviews() -> List[ReviewResponse]:
    return REVIEWS


def verify_signature(payload: bytes, signature: str) -> bool:
    if not settings.github_webhook_secret:
        return False
    sha_name, signature = signature.split("=")
    if sha_name != "sha256":
        return False
    mac = hmac.new(
        settings.github_webhook_secret.encode(), msg=payload, digestmod=hashlib.sha256
    )
    return hmac.compare_digest(mac.hexdigest(), signature)


@app.post("/webhook")
def webhook(
    payload: dict,
    x_hub_signature_256: str = Header(default=""),
    x_github_event: str = Header(default=""),
) -> dict:
    raw = str(payload).encode()
    if settings.github_webhook_secret:
        if not x_hub_signature_256 or not verify_signature(raw, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid signature")

    if x_github_event == "pull_request":
        action = payload.get("action")
        if action in {"opened", "synchronize", "reopened"}:
            pr = payload.get("pull_request", {})
            repo = payload.get("repository", {})
            pr_info = PRInfo(
                repo_full_name=repo.get("full_name", ""),
                pr_number=pr.get("number", 0),
                title=pr.get("title", ""),
                body=pr.get("body", ""),
                files=[],
                author=pr.get("user", {}).get("login"),
                url=pr.get("html_url"),
            )
            review = analyze_pr(pr_info)
            REVIEWS.insert(0, review)
    return {"ok": True}
