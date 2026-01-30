from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class PRFile(BaseModel):
    filename: str
    patch: Optional[str] = None


class PRInfo(BaseModel):
    repo_full_name: str
    pr_number: int
    title: str
    body: Optional[str] = None
    files: List[PRFile]
    author: Optional[str] = None
    url: Optional[str] = None


class GitHubReviewRequest(BaseModel):
    repo_full_name: str
    pr_number: int
    access_token: str


SeverityLevel = Literal["critical", "high", "medium", "low", "info"]


class ReviewFinding(BaseModel):
    title: str
    severity: SeverityLevel
    description: str
    suggestion: Optional[str] = None
    file: Optional[str] = None
    line: Optional[int] = None


class ReviewResponse(BaseModel):
    summary: str
    findings: List[ReviewFinding]
    score: int
    warnings: List[str] = Field(default_factory=list)


class ReviewRecord(BaseModel):
    id: str
    pr: PRInfo
    review: ReviewResponse
    source: str
    created_at: datetime
