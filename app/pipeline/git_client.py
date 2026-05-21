import os
from git import Repo


class GitClient:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

        token = os.getenv("GITHUB_TOKEN")
        repo_url = os.getenv("GITHUB_REPO")

        # Default remote name
        self.remote_name = "origin"

        # If token + repo URL exist, rewrite origin URL safely
        if token and repo_url:
            repo_clean = repo_url.replace("https://", "").replace("http://", "")
            authenticated_url = f"https://{token}@{repo_clean}"

            try:
                remote = self.repo.remote(self.remote_name)
                remote.set_url(authenticated_url)
            except Exception:
                # fallback if remote doesn't exist yet
                pass

    def commit_all(self, message: str):
        self.repo.git.add(all=True)
        return self.repo.index.commit(message)

    def push(self, branch: str):
        remote = self.repo.remote(self.remote_name)
        remote.push(refspec=f"{branch}:{branch}")