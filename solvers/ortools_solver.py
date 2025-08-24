from typing import Dict, Any, List

def solve(case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder: two-stage heuristic.
    If ortools is installed, you could replace with a CP-SAT FJSSP model.
    For now we mimic a better heuristic:
      1) pick min-time machine per operation,
      2) (optional) reorder ops by longest processing time first per machine before simulation (handled in evaluator).
    Returns assignments only; evaluator simulates the schedule.
    """
    try:
        import ortools  # noqa: F401
        # You can implement an advanced CP-SAT here if desired.
    except Exception:
        pass

    # Same as greedy for now (clear label so users know)
    assignments: List[Dict[str, str]] = []
    for job in case["jobs"]:
        j = job["job_id"]
        for op in job["operations"]:
            o = op["operation_id"]
            cands = [m for m in op["machines"] if m["time"] is not None]
            if not cands:
                continue
            chosen = min(cands, key=lambda m: m["time"])
            assignments.append({"job_id": j, "operation_id": o, "machine_id": chosen["id"]})
    return {"name": "ORToolsHeuristic(min-time)", "assignments": assignments}
