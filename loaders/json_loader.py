from typing import Any, Dict, List

def _already_standardized(obj: Dict[str, Any]) -> bool:
    return "case_id" in obj and "jobs" in obj and "metadata" in obj

def process_json(raw_json: Dict[str, Any], *, case_id: str = None, source="JSON Upload") -> dict:
    """
    Normalize a flexible raw JSON into standardized schema.
    Accepts either standardized schema or a loose format like sample.json.
    """
    if _already_standardized(raw_json):
        # enrich case_id or metadata if needed
        if case_id:
            raw_json["case_id"] = case_id
        return raw_json

    case_id = case_id or raw_json.get("CaseID", "JSON_Upload")
    jobs_std: List[Dict[str, Any]] = []

    for job in raw_json.get("Jobs", []):
        ops_std = []
        for op in job.get("Operations", []):
            machines_std = []
            for m in op.get("Machines", []):
                # tolerate missing/invalid time -> None
                time_val = m.get("ProcessingTime", None)
                try:
                    time_val = float(time_val) if time_val is not None else None
                except Exception:
                    time_val = None
                machines_std.append({"id": str(m.get("Machine")), "time": time_val})
            ops_std.append({"operation_id": str(op.get("OperationID")), "machines": machines_std})
        jobs_std.append({"job_id": str(job.get("JobID")), "operations": ops_std})

    return {
        "case_id": str(case_id),
        "jobs": jobs_std,
        "metadata": {
            "source": raw_json.get("Source", source),
            "objective": raw_json.get("Objective", "Minimize Makespan"),
            "created_by": raw_json.get("CreatedBy", "Campus Heilbronn")
        }
    }
