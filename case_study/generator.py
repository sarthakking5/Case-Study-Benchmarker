import json
from pathlib import Path
from loaders.validator import validate_case

def save_case_study(data: dict, name: str, out_dir: str = "data/standardized/") -> str:
    """Validate and save standardized case study."""
    case = validate_case(data)  # raises if invalid
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    path = Path(out_dir) / f"{name}.json"
    with open(path, "w") as f:
        json.dump(case.model_dump(), f, indent=4)
    return str(path)
