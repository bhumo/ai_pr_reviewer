from typing import List, Optional
from pydantic import BaseModel


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


class ReviewFinding(BaseModel):
    title: str
    severity: str
    description: str
    suggestion: Optional[str] = None
    file: Optional[str] = None
    line: Optional[int] = None


class ReviewResponse(BaseModel):
    summary: str
    findings: List[ReviewFinding]
    score: int
