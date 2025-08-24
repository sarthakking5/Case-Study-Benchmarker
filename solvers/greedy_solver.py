from typing import Dict, Any, List

def solve(case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Greedy: for each operation, pick the machine with the smallest processing time.
    """
    assignments: List[Dict[str, str]] = []
    for job in case["jobs"]:
        j = job["job_id"]
        for op in job["operations"]:
            o = op["operation_id"]
            if not op["machines"]:
                continue
            # choose machine with min time (ignoring None)
            candidates = [m for m in op["machines"] if m["time"] is not None]
            if not candidates:
                continue
            chosen = min(candidates, key=lambda m: m["time"])
            assignments.append({"job_id": j, "operation_id": o, "machine_id": chosen["id"]})
    return {"name": "GreedyMinProcTime", "assignments": assignments}
