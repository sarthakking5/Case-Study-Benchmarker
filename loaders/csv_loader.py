import pandas as pd
from typing import Optional

def process_csv(df: pd.DataFrame, *, case_id: str = "CSV_Upload", source="CSV Upload") -> dict:
    """
    Convert CSV into standardized JSON structure.
    Expected cols: JobID, OperationID, MachineID, ProcessingTime
    Handles missing and invalid processing times (set to None).
    Drops rows missing critical IDs.
    """
    required = ["JobID", "OperationID", "MachineID"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Drop rows missing critical IDs
    df = df.dropna(subset=required)

    jobs = []
    for job_id, job_df in df.groupby("JobID"):
        operations = []
        for op_id, op_df in job_df.groupby("OperationID"):
            machines = []
            for _, row in op_df.iterrows():
                time_val: Optional[float]
                try:
                    time_val = float(row["ProcessingTime"])
                    if pd.isna(time_val):
                        time_val = None
                except Exception:
                    time_val = None

                machines.append({
                    "id": str(row["MachineID"]),
                    "time": time_val
                })

            operations.append({"operation_id": str(op_id), "machines": machines})
        jobs.append({"job_id": str(job_id), "operations": operations})

    return {
        "case_id": str(case_id),
        "jobs": jobs,
        "metadata": {
            "source": source,
            "objective": "Minimize Makespan",
            "created_by": "Campus Heilbronn"
        }
    }
