from typing import List

from github import Github, GithubException

from app.config import settings
from app.models import PRFile, PRInfo


def _truncate_patch(patch: str) -> str:
    if not patch:
        return ""
    if len(patch) <= settings.max_patch_chars:
        return patch
    return f"{patch[:settings.max_patch_chars]}\n...[truncated to {settings.max_patch_chars} characters]"


def fetch_pr(access_token: str, repo_full_name: str, pr_number: int) -> PRInfo:
    try:
        gh = Github(access_token, per_page=100)
        repo = gh.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
    except GithubException as exc:  # pragma: no cover - relies on network/github
        raise ValueError(exc.data.get("message", "GitHub API error")) from exc

    files: List[PRFile] = []
    for index, f in enumerate(pr.get_files()):
        if index >= settings.max_files:
            break
        files.append(PRFile(filename=f.filename, patch=_truncate_patch(f.patch)))

    return PRInfo(
        repo_full_name=repo_full_name,
        pr_number=pr_number,
        title=pr.title,
        body=pr.body,
        files=files,
        author=pr.user.login if pr.user else None,
        url=pr.html_url,
    )
