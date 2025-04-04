import yaml
import os 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

if not os.path.isfile(CONFIG_PATH):
    raise FileNotFoundError(f"[config_loader]")

with open(CONFIG_PATH, "r") as f:
   config = yaml.safe_load(f)
