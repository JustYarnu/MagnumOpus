import os
import time
from git import Repo

REPO_PATH = "./"  
TEXT_FILE_PATH = "./bibel.txt"  
BRANCH_NAME = "main"
DELAY_SECONDS = 60
INTERVAL_LIMIT = 200
PUSH_INTERVAL = 400

def process_batch():
    if not os.path.exists(TEXT_FILE_PATH):
        print(f"Error: {TEXT_FILE_PATH} not found.")
        return

    try:
        repo = Repo(REPO_PATH)
    except Exception as e:
        print(f"Failed to initialize repository: {e}")
        return

    commit_count = 0

    for _ in range(INTERVAL_LIMIT):
        with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        while lines and not lines[-1].strip():
            lines.pop()

        if not lines:
            print("No more lines to process.")
            break

        commit_message = lines[0].strip()
        
        remaining_lines = lines[1:]

        with open(TEXT_FILE_PATH, "w", encoding="utf-8") as f:
            f.writelines(remaining_lines)

        if not commit_message:
            continue

        try:
            repo.git.add(all=True)
            repo.index.commit(commit_message)
            commit_count += 1
            print(f"Committed locally ({commit_count}/{INTERVAL_LIMIT}): '{commit_message}'")

            if commit_count % PUSH_INTERVAL == 0:
                print(f"Batch limit reached ({PUSH_INTERVAL} commits). Pushing to remote...")
                origin = repo.remote(name="origin")
                origin.push(refspec=f"{BRANCH_NAME}:{BRANCH_NAME}")
                
                print(f"Sleeping for {DELAY_SECONDS} seconds...")
                time.sleep(DELAY_SECONDS)

        except Exception as e:
            print(f"An error occurred during git operations: {e}")
            pass

    if commit_count % PUSH_INTERVAL != 0:
        try:
            print(f"Pushing final remainder of {commit_count % PUSH_INTERVAL} commits...")
            origin = repo.remote(name="origin")
            origin.push(refspec=f"{BRANCH_NAME}:{BRANCH_NAME}")
        except Exception as e:
            print(f"Failed to push final batch: {e}")

if __name__ == "__main__":
    process_batch()