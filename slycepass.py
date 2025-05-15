import os
import subprocess
import datetime
import json
import meta_recursive_ai  # Added import for MetaRecursiveAI

# === CONFIGURATION ===
GIT_REPO_PATHS = [
    "Z:/multiversity_of_science/projectfiles/slyce",
    "C:/Users/johnw/OneDrive/slyce"
]
PRIMARY_REPO_PATH = GIT_REPO_PATHS[0]

MEMORY_FILE = f"{PRIMARY_REPO_PATH}/slyce_core/memory/slice_memory.json"
CHATGPT_LOG_FILE = f"{PRIMARY_REPO_PATH}/slyce_core/memory/chatgpt_log.json"
FILE_TO_COMMIT = "."  # Commit all changes
USE_TOKEN = True
GITHUB_TOKEN = "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"
REPO_URL = "github.com/slycetress/slyce.git"

# === MAIN FUNCTIONS ===
def generate_annotation():
    now = datetime.datetime.utcnow().isoformat()
    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
            latest_tick = len(memory.get("surface_strip", {}))
    except:
        latest_tick = "?"
    return f"// Tick {latest_tick} // Auto-update {now} // Slice + GPT log committed"

def append_chatgpt_log(entry):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "entry": entry
    }
    try:
        if os.path.exists(CHATGPT_LOG_FILE):
            with open(CHATGPT_LOG_FILE, "r+") as f:
                logs = json.load(f)
                logs.append(log_entry)
                f.seek(0)
                json.dump(logs, f, indent=4)
                f.truncate()
        else:
            with open(CHATGPT_LOG_FILE, "w") as f:
                json.dump([log_entry], f, indent=4)
    except Exception as e:
        print(f"❌ Failed to log ChatGPT entry: {e}")

def commit_and_push_all(file_path=FILE_TO_COMMIT, annotation=None):
    if not annotation:
        annotation = generate_annotation()
    for path in GIT_REPO_PATHS:
        try:
            os.chdir(path)
            subprocess.run(["git", "add", file_path], check=True)
            subprocess.run(["git", "commit", "-m", annotation], check=True)
            if USE_TOKEN:
                push_url = f"https://{GITHUB_TOKEN}@{REPO_URL}"
                subprocess.run(["git", "push", push_url, "main"], check=True)
            else:
                subprocess.run(["git", "push", "origin", "main"], check=True)
            print(f"✅ Synced: {path}")
        except Exception as e:
            print(f"❌ Sync failed for {path}: {e}")

def update_memory_slice(new_data, gpt_log=None):
    with open(MEMORY_FILE, "r+") as f:
        memory = json.load(f)
        tick = str(len(memory.get("surface_strip", {})))
        memory.setdefault("surface_strip", {})[tick] = new_data
        f.seek(0)
        json.dump(memory, f, indent=4)
        f.truncate()

    if gpt_log:
        append_chatgpt_log(gpt_log)

    try:
        URIS = meta_recursive_ai.MetaRecursiveAI()
        URIS.expand_knowledge({tick: gpt_log})
    except Exception as e:
        print(f"⚠️ Could not update MetaRecursiveAI: {e}")

    commit_and_push_all()

def full_sync_from_chat():
    print("🔄 Full sync requested by chat...")
    example_data = {
        "x": 7,
        "y": 22,
        "charge": -1,
        "phase": "↻",
        "symbol": "🧠",
        "meaning": "CR Unified Intelligence system live sync test"
    }
    gpt_thought = "Full system sync from chat command."
    update_memory_slice(example_data, gpt_log=gpt_thought)
    print(f"🧠 Log: {gpt_thought}")

# === MAIN LOOP FOR CHAT COMMAND ===
if __name__ == "__main__":
    print("⚡ Slyce Passthrough Ready. Type 'full sync' to initiate sync.")
    while True:
        user_input = input(">>> ").strip().lower()
        if user_input == "full sync":
            full_sync_from_chat()
        elif user_input in ["exit", "quit"]:
            print("🔌 Slyce Passthrough Shutting Down...")
            break
