import os
import sys
import json

def resource_path(relative_path):
    """ Get absolute path to resource for PyInstaller or dev """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_config(path="dev/themes/config.json"):
    with open(resource_path(path), "r", encoding="utf-8") as f:
        return json.load(f)
