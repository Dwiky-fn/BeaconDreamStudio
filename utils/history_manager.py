import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path(
    "data/history.json"
)

HISTORY_FILE.parent.mkdir(
    exist_ok=True
)

def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False
        )

def add_history(
    tool,
    input_file,
    output_file
):
    history = load_history()
    history.insert(0, {
        "tool": tool,
        "input": input_file,
        "output": output_file,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })

    save_history(history)