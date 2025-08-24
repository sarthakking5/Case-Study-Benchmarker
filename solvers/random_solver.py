import random
from typing import Dict, Any, List

def solve(case: Dict[str, Any], seed: int = 42) -> Dict[str, Any]:
    random.seed(seed)
    assignments: List[Dict[str, str]] = []
    for job in case["jobs"]:
        j = job["job_id"]
        for op in job["operations"]:
            o = op["operation_id"]
            if not op["machines"]:
                continue
            chosen = random.choice(op["machines"])
            assignments.append({"job_id": j, "operation_id": o, "machine_id": chosen["id"]})
    return {"name": "RandomSolver", "assignments": assignments}
