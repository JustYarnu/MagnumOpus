from git import Repo

class GitClient:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

    def commit_all(self, message: str):
        self.repo.git.add(all=True)
        return self.repo.index.commit(message)

    def push(self, branch: str):
        origin = self.repo.remote(name="origin")
        origin.push(refspec=f"{branch}:{branch}")