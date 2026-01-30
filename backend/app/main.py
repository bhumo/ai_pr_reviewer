import hashlib
import hmac
from collections import deque
from datetime import datetime
from typing import Deque, List
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import GitHubReviewRequest, PRInfo, ReviewRecord, ReviewResponse
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

REVIEWS: Deque[ReviewRecord] = deque(maxlen=settings.review_history_size)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "openai_configured": bool(settings.openai_api_key),
        "model": settings.openai_model,
    }


def _store_review(pr: PRInfo, review: ReviewResponse, source: str) -> None:
    REVIEWS.appendleft(
        ReviewRecord(
            id=str(uuid4()),
            pr=pr,
            review=review,
            source=source,
            created_at=datetime.utcnow(),
        )
    )


@app.post("/review", response_model=ReviewResponse)
def review_pr(pr: PRInfo) -> ReviewResponse:
    review = analyze_pr(pr)
    _store_review(pr, review, source="direct")
    return review


@app.post("/review/github", response_model=ReviewResponse)
def review_pr_from_github(request: GitHubReviewRequest) -> ReviewResponse:
    try:
        pr = fetch_pr(request.access_token, request.repo_full_name, request.pr_number)
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=400, detail=f"Failed to fetch PR: {exc}") from exc

    review = analyze_pr(pr)
    _store_review(pr, review, source="github")
    return review


@app.get("/reviews", response_model=List[ReviewRecord])
def list_reviews() -> List[ReviewRecord]:
    return list(REVIEWS)


def verify_signature(payload: bytes, signature: str) -> bool:
    if not settings.github_webhook_secret:
        return False
    try:
        sha_name, signature = signature.split("=", 1)
    except ValueError:
        return False
    if sha_name != "sha256":
        return False
    mac = hmac.new(
        settings.github_webhook_secret.encode(), msg=payload, digestmod=hashlib.sha256
    )
    return hmac.compare_digest(mac.hexdigest(), signature)


@app.post("/webhook")
async def webhook(
    request: Request,
    x_hub_signature_256: str = Header(default=""),
    x_github_event: str = Header(default=""),
) -> dict:
    raw_body = await request.body()
    if settings.github_webhook_secret:
        if not x_hub_signature_256 or not verify_signature(raw_body, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = await request.json()
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from exc

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
            _store_review(pr_info, review, source="webhook")
    return {"ok": True}
