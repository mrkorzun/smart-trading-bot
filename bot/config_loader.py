import os
import yaml

def load_config(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()