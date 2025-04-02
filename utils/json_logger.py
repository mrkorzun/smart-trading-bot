import json
import os

SIGNALS_PATH = "signals/signals.json"

def save_signal(signal_dict):
    if not os.path.exists(SIGNALS_PATH):
        with open(SIGNALS_PATH, "w") as f:
            json.dump([], f)

    with open(SIGNALS_PATH, "r") as f:
        data = json.load(f)

    data.append(signal_dict)

    with open(SIGNALS_PATH, "w") as f:
        json.dump(data, f, indent=2)
