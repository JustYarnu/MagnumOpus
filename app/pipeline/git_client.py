import os
from git import Repo


class GitClient:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

        token = os.getenv("GITHUB_TOKEN")
        repo_url = os.getenv("GITHUB_REPO")

        if not repo_url:
            raise ValueError("GITHUB_REPO is not set")

        # Ensure clean HTTPS URL
        if repo_url.startswith("git@"):
            raise ValueError("SSH URLs are not supported. Use HTTPS format.")

        self.remote_name = "origin"

        if token:
            if repo_url.startswith("https://"):
                auth_url = repo_url.replace(
                    "https://",
                    f"https://{token}@"
                )
            else:
                # fallback safety
                auth_url = f"https://{token}@{repo_url}"
        else:
            auth_url = repo_url

        # Configure remote
        try:
            if self.remote_name in self.repo.remotes:
                remote = self.repo.remote(self.remote_name)
                remote.set_url(auth_url)
            else:
                self.repo.create_remote(self.remote_name, auth_url)
        except Exception:
            # If remote already exists but can't be modified cleanly
            pass

    def commit_all(self, message: str):
        self.repo.git.add(all=True)
        return self.repo.index.commit(message)

    def push(self, branch: str):
        remote = self.repo.remote(self.remote_name)
        remote.push(refspec=f"{branch}:{branch}")