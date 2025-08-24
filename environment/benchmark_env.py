import json
from typing import Callable, Dict, Any, List
from solvers import random_solver, greedy_solver, ortools_solver
from solvers.evaluator import simulate

class BenchmarkEnv:
    """
    Usage:
        env = BenchmarkEnv("data/standardized/SAMPLE_CSV.json")
        env.run_baselines()
        env.run_custom_solver(my_solver_fn)
    """
    def __init__(self, case_path: str):
        with open(case_path, "r") as f:
            self.case = json.load(f)
        self.case_path = case_path

    def run_baselines(self) -> List[Dict[str, Any]]:
        results = []
        for solver in [random_solver.solve, greedy_solver.solve, ortools_solver.solve]:
            s_out = solver(self.case)
            metrics = simulate(self.case, s_out["assignments"])
            results.append({
                "solver": s_out["name"],
                "makespan": metrics["makespan"],
                "num_tasks": metrics["num_tasks"]
            })
        return results

    def run_custom_solver(self, solver_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        s_out = solver_fn(self.case)
        metrics = simulate(self.case, s_out["assignments"])
        return {
            "solver": s_out.get("name", solver_fn.__name__),
            "makespan": metrics["makespan"],
            "num_tasks": metrics["num_tasks"]
        }
