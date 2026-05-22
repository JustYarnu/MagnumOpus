import os
from git import Repo


class GitClient:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_url = os.getenv("GITHUB_REPO")

        if not self.repo_url:
            raise ValueError(
                "Missing GITHUB_REPO environment variable"
            )

        if not self.token:
            raise ValueError(
                "Missing GITHUB_TOKEN environment variable"
            )

    def commit_all(self, message: str):
        self.repo.git.add(all=True)
        return self.repo.index.commit(message)

    def push(self, branch: str):
        auth_url = self.repo_url.replace(
            "https://",
            f"https://x-access-token:{self.token}@"
        )

        self.repo.git.push(
            auth_url,
            f"{branch}:{branch}"
        )