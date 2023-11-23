
import os


API_ID = 23315624
API_HASH = "2a9f6a9345d906df84bc2b071a802b88"


INPUT_DIR = "Input"
DEFAULT_SESSIONS_DIR = "session_files"

DOWNLOADED_MEDIA_DIR = "Downloads"


STARTUP_DIRS_TO_CREATE = [DEFAULT_SESSIONS_DIR, INPUT_DIR, DOWNLOADED_MEDIA_DIR]

for d in STARTUP_DIRS_TO_CREATE:
    os.makedirs(d, exist_ok=True)


# Create startup files
TARGET_GROUPS_FILE = f"{INPUT_DIR}/chat_ids.txt"

STARTUP_FILES = [TARGET_GROUPS_FILE]


for fi in STARTUP_FILES:
    if not os.path.exists(fi):
        with open(fi, "w", encoding="UTF-8") as _:
            pass

VIRCHUAL = bool(os.environ.get("VIRCHUAL", False))
