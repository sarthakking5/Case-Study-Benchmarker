import json
from pathlib import Path
from typing import List

def list_cases(dir_path: str = "data/standardized/") -> List[str]:
    return sorted([str(p) for p in Path(dir_path).glob("*.json")])

def load_case(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)
