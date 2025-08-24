import pandas as pd

def to_flat_table(case: dict) -> pd.DataFrame:
    """
    Create a flat (Job,Operation,Machine,Time) DataFrame view from standardized case.
    """
    rows = []
    for job in case["jobs"]:
        for op in job["operations"]:
            for m in op["machines"]:
                rows.append({
                    "JobID": job["job_id"],
                    "OperationID": op["operation_id"],
                    "MachineID": m["id"],
                    "ProcessingTime": m["time"]
                })
    return pd.DataFrame(rows)
