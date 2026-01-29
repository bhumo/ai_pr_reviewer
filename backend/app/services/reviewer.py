from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.models import PRInfo, ReviewFinding, ReviewResponse
from app.config import settings


SYSTEM_PROMPT = """
You are an automated pull request reviewer. Analyze the PR for bugs, code smells, and style violations.
Return a concise summary, severity-tagged findings, and a 0-100 quality score.
""".strip()


def build_prompt(pr: PRInfo) -> str:
    files_section = "\n\n".join(
        f"File: {f.filename}\nPatch:\n{f.patch or ''}" for f in pr.files
    )
    return f"""
Title: {pr.title}
Description: {pr.body or ''}
Author: {pr.author or ''}
URL: {pr.url or ''}
Files:\n{files_section}
""".strip()


def analyze_pr(pr: PRInfo) -> ReviewResponse:
    if not settings.openai_api_key:
        return ReviewResponse(
            summary="OpenAI API key not configured.",
            findings=[],
            score=0,
        )

    model = ChatOpenAI(api_key=settings.openai_api_key, model="gpt-4o-mini", temperature=0.2)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Analyze the following PR:\n{input}"),
        ]
    )
    chain = prompt | model
    response = chain.invoke({"input": build_prompt(pr)})

    content = response.content
    return ReviewResponse(
        summary=content[:4000],
        findings=[
            ReviewFinding(
                title="Summary",
                severity="info",
                description=content[:4000],
            )
        ],
        score=80,
    )
