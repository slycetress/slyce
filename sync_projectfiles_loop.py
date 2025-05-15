import time
import subprocess

while True:
    print("Running GitHub sync script...")
    subprocess.call(["bash", "sync_projectfiles_to_github_win_logged.sh"])
    print("Sync complete. Waiting 30 minutes...")
    time.sleep(1800)  # 30 minutes
