from typing import Dict, List, Tuple, Any

def simulate(case: Dict[str, Any], assignments: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Discrete-event style simulation:
    - Enforces job precedence (O1 -> O2 -> ...)
    - Machines are unary-capacity (one job at a time)
    - Processing times taken from case; if missing (None), operation is skipped in makespan calc
    Returns schedule with start/finish times and KPIs.
    """
    # Build quick lookup: proc_time[(job, op, machine)] -> time
    time_lu = {}
    for job in case["jobs"]:
        j = job["job_id"]
        for op in job["operations"]:
            o = op["operation_id"]
            for m in op["machines"]:
                time_lu[(j, o, m["id"])] = m["time"]

    # Machine & job ready times
    m_ready = {}      # machine_id -> time
    j_ready = {}      # job_id -> time
    ops_order = {}    # job_id -> sorted operation ids (string sort works if O1,O2,...)

    for job in case["jobs"]:
        j_ready[job["job_id"]] = 0.0
        ops_order[job["job_id"]] = [op["operation_id"] for op in job["operations"]]

    schedule = []
    for a in assignments:
        j, o, m = a["job_id"], a["operation_id"], a["machine_id"]
        pt = time_lu.get((j, o, m), None)
        if pt is None:
            # skip unprocessable op (no time)
            continue

        start = max(m_ready.get(m, 0.0), j_ready.get(j, 0.0))
        finish = start + pt
        m_ready[m] = finish
        j_ready[j] = finish
        schedule.append({"job_id": j, "operation_id": o, "machine_id": m, "start": start, "finish": finish, "time": pt})

    makespan = max((task["finish"] for task in schedule), default=0.0)
    machine_util = _machine_utilization(schedule)
    return {
        "makespan": makespan,
        "machine_utilization": machine_util,
        "num_tasks": len(schedule),
        "schedule": schedule
    }

def _machine_utilization(schedule: List[Dict[str, Any]]) -> Dict[str, float]:
    if not schedule:
        return {}
    # utilization = busy_time / makespan (per machine)
    by_m = {}
    for t in schedule:
        m = t["machine_id"]
        by_m.setdefault(m, 0.0)
        by_m[m] += t["time"] or 0.0
    makespan = max(t["finish"] for t in schedule)
    return {m: (busy / makespan if makespan > 0 else 0.0) for m, busy in by_m.items()}
