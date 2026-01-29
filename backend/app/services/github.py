from typing import List
from github import Github
from app.models import PRFile, PRInfo


def fetch_pr(access_token: str, repo_full_name: str, pr_number: int) -> PRInfo:
    gh = Github(access_token)
    repo = gh.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)
    files: List[PRFile] = []
    for f in pr.get_files():
        files.append(PRFile(filename=f.filename, patch=f.patch))

    return PRInfo(
        repo_full_name=repo_full_name,
        pr_number=pr_number,
        title=pr.title,
        body=pr.body,
        files=files,
        author=pr.user.login if pr.user else None,
        url=pr.html_url,
    )
