import sys
import subprocess

# ---- Config ----
input_file = "data/raw/sample_case.json"
case_id = "TestCase_FullPipeline"
runner_path = "environment/runner.py"

# Get the Python interpreter for the current venv
python_executable = sys.executable

# ---- Step 1: Standardize ----
print("➡️  Step 1: Standardizing raw CSV/JSON...")
subprocess.run([
    python_executable, runner_path, "standardize",
    input_file,
    "--case_id", case_id
], check=True)

# ---- Step 2: List standardized cases ----
print("\n➡️  Step 2: Listing standardized cases...")
subprocess.run([
    python_executable, runner_path, "list"
], check=True)

# ---- Step 3: Run baseline solvers ----
standardized_case_path = f"data/standardized/{case_id}.json"
print(f"\n➡️  Step 3: Running baseline solvers on {standardized_case_path}...")
subprocess.run([
    python_executable, runner_path, "run", standardized_case_path
], check=True)
