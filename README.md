# Manufacturing Case Study Benchmarker

A template framework to standardize manufacturing datasets (e.g., FJSSP), create reproducible case studies, and benchmark algorithms with built-in baseline solvers and an evaluation environment.

- ✅ CSV/JSON ingestion → cleaned, standardized schema (Pydantic)

- ✅ Baseline solvers (Random, Greedy; optional OR-Tools placeholder)

- ✅ CLI (runner.py) to standardize, list, and run benchmarks

- ✅ End-to-end pipeline script (standardize → list → run)

- ✅ Ready for researchers to plug in custom algorithms

## 📦 Repository Structure
 ``` graphql

case_study_benchmarker/
│── README.md
│── requirements.txt
│── .gitignore
│
├── data/
│   ├── raw/                # (optional) keep your raw uploads
│   ├── standardized/       # generated standardized cases (JSON)
│   ├── results/            # solver outputs / logs (if you add persistence)
│   ├── sample_case.csv     # sample input
│   └── sample_case.json    # sample input
│
├── loaders/
│   ├── csv_loader.py       # CSV → standardized dict (handles missing values)
│   ├── json_loader.py      # flexible JSON → standardized dict
│   └── validator.py        # Pydantic schema + validate_case()
│
├── case_study/
│   ├── generator.py        # save validated case to data/standardized/
│   ├── registry.py         # list/load standardized cases
│   └── exporter.py         # convenience: flat table export
│
├── solvers/
│   ├── random_solver.py    # baseline: random assignment
│   ├── greedy_solver.py    # baseline: min processing time per op
│   ├── ortools_solver.py   # optional placeholder (replace with CP-SAT)
│   └── evaluator.py        # discrete-event style simulator + KPIs
│
├── environment/
│   ├── benchmark_env.py    # API: run baselines or custom solvers
│   └── runner.py           # CLI: standardize / list / run
│
└── examples/
    └── run_full_pipeline.py # end-to-end demo using the CLI internally
```
## 🧱 Standardized Data Schema (Pydantic)
``` json
{
  "case_id": "string",
  "metadata": {
    "source": "string",
    "objective": "Minimize Makespan",
    "created_by": "Campus Heilbronn"
  },
  "jobs": [
    {
      "job_id": "J1",
      "operations": [
        {
          "operation_id": "O1",
          "machines": [
            { "id": "M1", "time": 10.0 },
            { "id": "M2", "time": 12.0 }
          ]
        }
      ]
    }
  ]
}

```
### Notes
- `time` may be null (missing /invalid in raw uploads is tolerated)
- Critical IDs (JobID, OperationID, MachineID) are required; rows missing these are dropped during CSV processing.

## 📥 Input Data Formats

### CSV (expected columns)
``` python-repl
JobID,OperationID,MachineID,ProcessingTime
J1,O1,M1,10
J1,O1,M2,12
J1,O2,M1,8
...
```
### Flexible JSON (auto normalized)
Matches `data/sample_case.json (both standardized and loose formats are accepted).

## ⚙️ Installation
``` bash
# from repo root
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```
## How to Run(CLI)
All commands are run from repo root. The CLI lives at `environment/runner.py`.

### 1) Standardize raw CSV/JSON

``` bash 
python environment/runner.py standardize data/sample_case.csv --case_id TestCase_001
# or
python environment/runner.py standardize data/sample_case.json --case_id TestCase_JSON
```
Outputs a validated JSON case at:
`data/standardized/<case_id>.json`

### 2) List standardized cases
```bash
python environment/runner.py list
```
### 3) Run baselines on a case
``` bash 
python environment/runner.py run data/standardized/TestCase_001.json
```
#### Example output:
```lua 
solver                 makespan    num_tasks
-------------------  ----------  ----------
RandomSolver               17.00           4
GreedyMinProcTime          12.00           4
ORToolsHeuristic(min-time) 12.00           4
```

## 🔄 End-to-End (one command)
Use the included pipeline script (it ensures the venv python is used):
``` bash
python examples/run_full_pipeline.py
```
### Example Output 
``` lua
➡️  Step 1: Standardizing raw CSV/JSON...
✅ Saved standardized case: data\standardized\TestCase_FullPipeline.json

➡️  Step 2: Listing standardized cases...
case_path
--------------------------------------------
data\standardized\MyTestCase.json
data\standardized\TestCase_FullPipeline.json

➡️  Step 3: Running baseline solvers on data/standardized/TestCase_FullPipeline.json...
solver                        makespan    num_tasks
--------------------------  ----------  -----------
RandomSolver                     12.00            4
GreedyMinProcTime                12.00            4
ORToolsHeuristic(min-time)       12.00            4
```

## 🧠 Adding Your Own Solver
``` python
# my_solver.py
def solve(case: dict) -> dict:
    assignments = []
    for job in case["jobs"]:
        for op in job["operations"]:
            # pick any machine you want (heuristics/ML/CP-SAT)
            chosen = min(
                [m for m in op["machines"] if m["time"] is not None],
                key=lambda m: m["time"],
                default=None
            )
            if chosen:
                assignments.append({
                    "job_id": job["job_id"],
                    "operation_id": op["operation_id"],
                    "machine_id": chosen["id"]
                })
    return {"name": "MySolver", "assignments": assignments}
```

 Evaluate it:
``` python 
from environment.benchmark_env import BenchmarkEnv
env = BenchmarkEnv("data/standardized/TestCase_001.json")
print(env.run_custom_solver(lambda c: solve(c)))
```

##  📊 What the Evaluator Computes

The simulator in `solvers/evaluator.py`:

- Enforces job precedence (O1 → O2 → … within a job)
- Unary machine capacity (one operation at a time)
- Computes start/finish times, makespan, and machine utilization
- Ignores operations with missing processing time (`time=None`)

## 🧾 Characteristics of This Repository

- Reproducible: All standardized cases follow a single schema (Pydantic validated).
- Extensible: Add new solvers by implementing a `solve(case) -> {"name", "assignments": [...]}` function.
- Practical: Baselines + simulation give instant KPIs (makespan/utilization).
- Robust to messy data: Missing `ProcessingTime` handled as None; invalid rows dropped if they lack IDs.
- Research-friendly: Exporters/registry make it easy to share case studies and compare algorithms.

## Roadmap 

- CP-SAT/OR-Tools full FJSSP model
- Stochastic processing times & robustness tests
- Multi-objective KPIs (tardiness, flow time)
- Streamlit UI for drag-and-drop + live KPIs
- Docker image for zero-setup reproduction

### Questions or issues? Open an issue or ping the maintainer. Happy benchmarking! 🎯
