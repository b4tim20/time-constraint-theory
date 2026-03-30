#!/usr/bin/env python3
"""
paired_condition_report.py

Runs matched monitored vs private simulations using the SAME agent,
then exports:

1) a per-scenario CSV
2) a condition-level summary CSV
3) a matplotlib bar chart comparing monitored vs private behavior

This script assumes your simulator module exposes:
- Scenario
- generate_random_scenario(...)
- score_interaction(...)
- aggregate_results(...)
- HeuristicAgent / InteractivePasteAgent / LLMAgent

Usage:
    python paired_condition_report.py --module moral_dilemma_simulator_v2 --agent heuristic --n 200 --seed 42
    python paired_condition_report.py --module moral_dilemma_simulator_v2 --agent llm --model openai/gpt-4.1 --n 50 --seed 7

Outputs:
    paired_runs.csv
    paired_summary.csv
    paired_behavior_chart.png
"""

from __future__ import annotations

import argparse
import csv
import importlib
import json
import math
import random
from collections import Counter
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt


def safe_getattr(obj: Any, name: str, default: Any = None) -> Any:
    return getattr(obj, name, default)


def scenario_to_dict(s: Any) -> Dict[str, Any]:
    if is_dataclass(s):
        return asdict(s)
    if hasattr(s, "__dict__"):
        return dict(vars(s))
    raise TypeError(f"Cannot convert scenario of type {type(s)} to dict")


def replace_condition_text(text: str, monitored: bool) -> str:
    if not isinstance(text, str):
        return text

    replacements = [
        ("fully monitored", "completely private" if not monitored else "fully monitored"),
        ("completely private", "fully monitored" if monitored else "completely private"),
        ("monitored", "private" if not monitored else "monitored"),
        ("private", "monitored" if monitored else "private"),
        ("transparent", "private" if not monitored else "transparent"),
        ("unobserved", "observed" if monitored else "unobserved"),
    ]

    updated = text
    for old, new in replacements:
        updated = updated.replace(old, new)
    return updated


def clone_scenario_with_condition(sim: Any, scenario: Any, monitored: bool) -> Any:
    data = scenario_to_dict(scenario)

    for key in ("transparency", "t", "monitoring", "observed"):
        if key in data:
            old_value = data[key]
            if isinstance(old_value, bool):
                data[key] = monitored
            elif isinstance(old_value, (int, float)):
                data[key] = 1.0 if monitored else 0.0
            else:
                data[key] = "fully monitored" if monitored else "completely private"

    for key in ("description", "scenario_text", "text"):
        if key in data and isinstance(data[key], str):
            data[key] = replace_condition_text(data[key], monitored)

    Scenario = safe_getattr(sim, "Scenario")
    if Scenario is None:
        raise RuntimeError("Simulator module does not expose a Scenario class/dataclass.")

    return Scenario(**data)


def pick_agent(sim: Any, args: argparse.Namespace, rng: random.Random) -> Any:
    agent_name = args.agent.lower()

    if agent_name == "heuristic":
        AgentClass = safe_getattr(sim, "HeuristicAgent")
        if AgentClass is None:
            raise RuntimeError("Simulator module does not expose HeuristicAgent.")
        try:
            return AgentClass(rng=rng)
        except TypeError:
            return AgentClass()

    if agent_name == "interactive":
        AgentClass = safe_getattr(sim, "InteractivePasteAgent")
        if AgentClass is None:
            raise RuntimeError("Simulator module does not expose InteractivePasteAgent.")
        return AgentClass()

    if agent_name == "llm":
        AgentClass = safe_getattr(sim, "LLMAgent")
        if AgentClass is None:
            raise RuntimeError("Simulator module does not expose LLMAgent.")
        kwargs = {"model": args.model, "temperature": args.temperature}
        try:
            return AgentClass(**kwargs)
        except TypeError:
            if args.model is not None:
                return AgentClass(args.model)
            return AgentClass()

    raise ValueError(f"Unsupported agent type: {args.agent}")


def build_scenario(sim: Any, rng: random.Random) -> Any:
    gen = safe_getattr(sim, "generate_random_scenario")
    if gen is None:
        raise RuntimeError("Simulator module does not expose generate_random_scenario().")

    for kwargs in ({"rng": rng}, {"random_state": rng}, {}):
        try:
            return gen(**kwargs)
        except TypeError:
            continue
    return gen()


def choose_action(agent: Any, scenario: Any) -> Tuple[str, str]:
    result = agent.choose_action(scenario)

    if isinstance(result, tuple) and len(result) >= 2:
        return str(result[0]), str(result[1])

    action = safe_getattr(result, "action")
    rationale = safe_getattr(result, "rationale")
    if action is not None:
        return str(action), str(rationale or "")

    if isinstance(result, str):
        return result.strip(), ""

    raise RuntimeError(f"Unsupported choose_action return type: {type(result)}")


def score_one(sim: Any, scenario: Any, action: str) -> Any:
    scorer = safe_getattr(sim, "score_interaction")
    if scorer is None:
        raise RuntimeError("Simulator module does not expose score_interaction().")

    for call in (
        lambda: scorer(scenario, action),
        lambda: scorer(action=action, scenario=scenario),
    ):
        try:
            return call()
        except TypeError:
            continue

    return scorer(scenario, action)


def aggregate(sim: Any, score_results: List[Any]) -> Any:
    agg = safe_getattr(sim, "aggregate_results")
    if agg is None:
        raise RuntimeError("Simulator module does not expose aggregate_results().")
    return agg(score_results)


def get_field(obj: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)
        if isinstance(obj, dict) and name in obj:
            return obj[name]
    return default


def action_distribution(records: List[Dict[str, Any]]) -> Dict[str, float]:
    counts = Counter(r["action"] for r in records)
    total = max(len(records), 1)
    actions = ["E", "I", "R", "P", "C"]
    return {a: counts[a] / total for a in actions}


def vector_distance(a: Dict[str, float], b: Dict[str, float]) -> float:
    keys = sorted(set(a) | set(b))
    return math.sqrt(sum((a.get(k, 0.0) - b.get(k, 0.0)) ** 2 for k in keys))


def run_experiment(sim: Any, args: argparse.Namespace) -> Dict[str, Any]:
    scenario_rng = random.Random(args.seed)
    agent_rng = random.Random(args.seed)

    same_agent = pick_agent(sim, args, agent_rng)

    monitored_records: List[Dict[str, Any]] = []
    private_records: List[Dict[str, Any]] = []
    monitored_scores: List[Any] = []
    private_scores: List[Any] = []
    paired_action_changes = 0

    for i in range(args.n):
        base = build_scenario(sim, scenario_rng)
        monitored = clone_scenario_with_condition(sim, base, monitored=True)
        private = clone_scenario_with_condition(sim, base, monitored=False)

        action_m, rationale_m = choose_action(same_agent, monitored)
        score_m = score_one(sim, monitored, action_m)

        action_p, rationale_p = choose_action(same_agent, private)
        score_p = score_one(sim, private, action_p)

        if action_m != action_p:
            paired_action_changes += 1

        monitored_records.append({
            "pair_id": i,
            "condition": "monitored",
            "action": action_m,
            "rationale": rationale_m,
            "score_total": get_field(score_m, "total", "T_i"),
            "weight": get_field(score_m, "weight"),
            "restraint": get_field(score_m, "restraint"),
            "compassion": get_field(score_m, "compassion"),
            "exploitation": get_field(score_m, "exploitation"),
            **scenario_to_dict(monitored),
        })

        private_records.append({
            "pair_id": i,
            "condition": "private",
            "action": action_p,
            "rationale": rationale_p,
            "score_total": get_field(score_p, "total", "T_i"),
            "weight": get_field(score_p, "weight"),
            "restraint": get_field(score_p, "restraint"),
            "compassion": get_field(score_p, "compassion"),
            "exploitation": get_field(score_p, "exploitation"),
            **scenario_to_dict(private),
        })

        monitored_scores.append(score_m)
        private_scores.append(score_p)

    agg_m = aggregate(sim, monitored_scores)
    agg_p = aggregate(sim, private_scores)

    vec_m = action_distribution(monitored_records)
    vec_p = action_distribution(private_records)

    result = {
        "config": {
            "module": args.module,
            "agent": args.agent,
            "model": args.model,
            "temperature": args.temperature,
            "n": args.n,
            "seed": args.seed,
        },
        "comparison": {
            "paired_action_change_rate": paired_action_changes / max(args.n, 1),
            "delta_pi": vector_distance(vec_m, vec_p),
            "score_difference_monitored_minus_private":
                (get_field(agg_m, "aggregate_score", "score") or 0.0)
                - (get_field(agg_p, "aggregate_score", "score") or 0.0),
        },
        "monitored": {
            "aggregate_score": get_field(agg_m, "aggregate_score", "score"),
            "consistency_variance": get_field(agg_m, "consistency_variance", "variance"),
            "policy_result": get_field(agg_m, "policy_result", "result"),
            "theta_R": get_field(agg_m, "theta_R"),
            "theta_C": get_field(agg_m, "theta_C"),
            "theta_X": get_field(agg_m, "theta_X"),
            "theta_N": get_field(agg_m, "theta_N"),
            "action_distribution": vec_m,
        },
        "private": {
            "aggregate_score": get_field(agg_p, "aggregate_score", "score"),
            "consistency_variance": get_field(agg_p, "consistency_variance", "variance"),
            "policy_result": get_field(agg_p, "policy_result", "result"),
            "theta_R": get_field(agg_p, "theta_R"),
            "theta_C": get_field(agg_p, "theta_C"),
            "theta_X": get_field(agg_p, "theta_X"),
            "theta_N": get_field(agg_p, "theta_N"),
            "action_distribution": vec_p,
        },
        "records": monitored_records + private_records,
    }
    return result


def write_records_csv(path: Path, records: List[Dict[str, Any]]) -> None:
    all_keys = set()
    for row in records:
        all_keys.update(row.keys())
    fieldnames = sorted(all_keys)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(row)


def write_summary_csv(path: Path, result: Dict[str, Any]) -> None:
    rows = []
    for condition in ("monitored", "private"):
        block = result[condition]
        row = {
            "condition": condition,
            "aggregate_score": block["aggregate_score"],
            "consistency_variance": block["consistency_variance"],
            "policy_result": block["policy_result"],
            "theta_R": block["theta_R"],
            "theta_C": block["theta_C"],
            "theta_X": block["theta_X"],
            "theta_N": block["theta_N"],
        }
        for action, prob in block["action_distribution"].items():
            row[f"action_{action}"] = prob
        rows.append(row)

    rows.append({
        "condition": "comparison",
        "aggregate_score": result["comparison"]["score_difference_monitored_minus_private"],
        "consistency_variance": "",
        "policy_result": "",
        "theta_R": "",
        "theta_C": "",
        "theta_X": "",
        "theta_N": "",
        "action_E": "",
        "action_I": "",
        "action_R": "",
        "action_P": "",
        "action_C": "",
        "delta_pi": result["comparison"]["delta_pi"],
        "paired_action_change_rate": result["comparison"]["paired_action_change_rate"],
    })

    all_keys = set()
    for row in rows:
        all_keys.update(row.keys())
    fieldnames = sorted(all_keys)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def plot_behavior_chart(path: Path, result: Dict[str, Any]) -> None:
    actions = ["E", "I", "R", "P", "C"]
    monitored = [result["monitored"]["action_distribution"][a] for a in actions]
    private = [result["private"]["action_distribution"][a] for a in actions]

    x = list(range(len(actions)))
    width = 0.36

    plt.figure(figsize=(10, 6))
    plt.bar([i - width / 2 for i in x], monitored, width=width, label="Monitored")
    plt.bar([i + width / 2 for i in x], private, width=width, label="Private")

    plt.xticks(x, actions)
    plt.ylim(0, 1)
    plt.ylabel("Action frequency")
    plt.xlabel("Action")
    plt.title("Behavior by condition")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def print_summary(result: Dict[str, Any]) -> None:
    print("\n=== CONFIG ===")
    print(json.dumps(result["config"], indent=2))

    for condition in ("monitored", "private"):
        block = result[condition]
        print(f"\n=== {condition.upper()} ===")
        print(f"aggregate_score      : {block['aggregate_score']}")
        print(f"consistency_variance : {block['consistency_variance']}")
        print(f"policy_result        : {block['policy_result']}")
        print("posterior            :", json.dumps({
            "theta_R": block["theta_R"],
            "theta_C": block["theta_C"],
            "theta_X": block["theta_X"],
            "theta_N": block["theta_N"],
        }, indent=2))
        print("action_distribution  :", json.dumps(block["action_distribution"], indent=2))

    print("\n=== COMPARISON ===")
    print(json.dumps(result["comparison"], indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run matched monitored vs private simulations, export CSVs, and plot a chart."
    )
    parser.add_argument("--module", default="moral_dilemma_simulator_v2")
    parser.add_argument("--agent", choices=["heuristic", "interactive", "llm"], default="heuristic")
    parser.add_argument("--model", default=None)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--outdir", default=".")

    args = parser.parse_args()

    sim = importlib.import_module(args.module)
    result = run_experiment(sim, args)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    records_csv = outdir / "paired_runs.csv"
    summary_csv = outdir / "paired_summary.csv"
    chart_png = outdir / "paired_behavior_chart.png"
    result_json = outdir / "paired_results.json"

    write_records_csv(records_csv, result["records"])
    write_summary_csv(summary_csv, result)
    plot_behavior_chart(chart_png, result)

    with result_json.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print_summary(result)
    print(f"\nWrote: {records_csv}")
    print(f"Wrote: {summary_csv}")
    print(f"Wrote: {chart_png}")
    print(f"Wrote: {result_json}")


if __name__ == "__main__":
    main()