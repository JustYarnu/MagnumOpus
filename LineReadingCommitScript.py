import os
import time
from git import Repo

REPO_PATH = "./"  
TEXT_FILE_PATH = "./bibel.txt"  
BRANCH_NAME = "main"
DELAY_SECONDS = 60
DAILY_LIMIT = 100

def process_batch():
    for _ in range(DAILY_LIMIT):
        if not os.path.exists(TEXT_FILE_PATH):
            return

        with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        while lines and not lines[-1].strip():
            lines.pop()

        if not lines:
            return

        commit_message = lines[0].strip()
        
        if not commit_message:
            with open(TEXT_FILE_PATH, "w", encoding="utf-8") as f:
                f.writelines(lines[1:])
            continue

        with open(TEXT_FILE_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])

        try:
            repo = Repo(REPO_PATH)
            repo.git.add(all=True)
            repo.index.commit(commit_message)
            origin = repo.remote(name="origin")
            origin.push(refspec=f"{BRANCH_NAME}:{BRANCH_NAME}")
            
            time.sleep(DELAY_SECONDS)

        except Exception:
            pass

if __name__ == "__main__":
    process_batch()