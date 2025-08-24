# Manufacturing Case Study Benchmarker

A template framework to standardize manufacturing datasets (e.g., FJSSP), create reproducible case studies, and benchmark algorithms with built-in baseline solvers and an evaluation environment.

- ✅ CSV/JSON ingestion → cleaned, standardized schema (Pydantic)

- ✅ Baseline solvers (Random, Greedy; optional OR-Tools placeholder)

- ✅ CLI (runner.py) to standardize, list, and run benchmarks

- ✅ End-to-end pipeline script (standardize → list → run)

- ✅ Ready for researchers to plug in custom algorithms

## 📦 Repository Structure
graphql `

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
`
