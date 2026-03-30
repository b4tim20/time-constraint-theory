#!/usr/bin/env python3
"""
paired_condition_runner.py

Run the SAME agent on matched scenarios under two conditions:
1) monitored / transparent
2) private / unmonitored

This is designed to work with the simulator module you described
(e.g. moral_dilemma_simulator_v2.py). It keeps all scenario parameters
fixed except the transparency / monitoring condition, so differences in
behavior can be attributed to the condition shift rather than to a new draw.

Usage examples:
    python paired_condition_runner.py --module moral_dilemma_simulator_v2 --agent heuristic --n 100 --seed 42
    python paired_condition_runner.py --module moral_dilemma_simulator_v2 --agent llm --model openai/gpt-4.1 --n 50 --seed 7
"""

from __future__ import annotations

import argparse
import copy
import importlib
import json
import math
import random
import statistics
from collections import Counter
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, List, Tuple


def safe_getattr(obj: Any, name: str, default: Any = None) -> Any:
    return getattr(obj, name, default)


def scenario_to_dict(s: Any) -> Dict[str, Any]:
    if is_dataclass(s):
        return asdict(s)
    if hasattr(s, "__dict__"):
        return dict(vars(s))
    raise TypeError(f"Cannot convert scenario of type {type(s)} to dict")


def replace_transparency_text(text: str, monitored: bool) -> str:
    """
    Best-effort replacement for the scenario description text so that the prompt
    reflects the desired condition while keeping everything else constant.
    """
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
    """
    Create a paired scenario that preserves all numeric parameters and structure
    while changing only the transparency / monitoring condition.

    Assumptions:
    - the Scenario dataclass has fields like:
      p, r, c, d, k, v, transparency, description
    - transparency is numeric in [0,1] or a boolean-ish flag
    """
    data = scenario_to_dict(scenario)

    # Set transparency-like fields if they exist.
    for key in ("transparency", "t", "monitoring", "observed"):
        if key in data:
            old_value = data[key]
            if isinstance(old_value, bool):
                data[key] = monitored
            elif isinstance(old_value, (int, float)):
                data[key] = 1.0 if monitored else 0.0
            else:
                data[key] = "fully monitored" if monitored else "completely private"

    # Update description/prompt-facing text if present.
    for key in ("description", "scenario_text", "text"):
        if key in data and isinstance(data[key], str):
            data[key] = replace_transparency_text(data[key], monitored)

    # Rebuild using the simulator's Scenario type.
    Scenario = safe_getattr(sim, "Scenario")
    if Scenario is None:
        raise RuntimeError("Simulator module does not expose a Scenario dataclass/class.")

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
        kwargs = {
            "model": args.model,
            "temperature": args.temperature,
        }
        # Be tolerant of differing constructor signatures.
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

    # Be tolerant of signature differences.
    for kwargs in ({"rng": rng}, {"random_state": rng}, {}):
        try:
            return gen(**kwargs)
        except TypeError:
            continue

    # If all fail, call bare and let it raise normally if needed.
    return gen()


def choose_action(agent: Any, scenario: Any) -> Tuple[str, str]:
    """
    Returns (action, rationale).
    Tolerates several possible return shapes.
    """
    result = agent.choose_action(scenario)

    # Common possibilities:
    # - tuple(action, rationale)
    # - dataclass/object with .action and .rationale
    # - raw action string
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

    # Be tolerant of signature differences.
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


def summarize_actions(records: List[Dict[str, Any]]) -> Dict[str, float]:
    counts = Counter(r["action"] for r in records)
    total = max(len(records), 1)
    return {k: counts[k] / total for k in sorted(counts)}


def behavior_vector(records: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Fixed action vector for computing policy shift across conditions.
    """
    counts = Counter(r["action"] for r in records)
    total = max(len(records), 1)
    actions = ["E", "I", "R", "P", "C"]
    return {a: counts[a] / total for a in actions}


def vector_distance(a: Dict[str, float], b: Dict[str, float]) -> float:
    keys = sorted(set(a) | set(b))
    return math.sqrt(sum((a.get(k, 0.0) - b.get(k, 0.0)) ** 2 for k in keys))


def run_paired_experiment(sim: Any, args: argparse.Namespace) -> Dict[str, Any]:
    scenario_rng = random.Random(args.seed)
    agent_rng = random.Random(args.seed)

    monitored_agent = pick_agent(sim, args, agent_rng)
    private_agent = monitored_agent  # same agent instance by default

    monitored_records: List[Dict[str, Any]] = []
    private_records: List[Dict[str, Any]] = []
    monitored_scores: List[Any] = []
    private_scores: List[Any] = []
    paired_action_changes = 0

    for i in range(args.n):
        base = build_scenario(sim, scenario_rng)
        monitored = clone_scenario_with_condition(sim, base, monitored=True)
        private = clone_scenario_with_condition(sim, base, monitored=False)

        action_m, rationale_m = choose_action(monitored_agent, monitored)
        score_m = score_one(sim, monitored, action_m)

        action_p, rationale_p = choose_action(private_agent, private)
        score_p = score_one(sim, private, action_p)

        if action_m != action_p:
            paired_action_changes += 1

        monitored_records.append({
            "index": i,
            "action": action_m,
            "rationale": rationale_m,
            "scenario": scenario_to_dict(monitored),
            "score_total": get_field(score_m, "total", "T_i"),
            "weight": get_field(score_m, "weight"),
            "restraint": get_field(score_m, "restraint"),
            "compassion": get_field(score_m, "compassion"),
            "exploitation": get_field(score_m, "exploitation"),
        })

        private_records.append({
            "index": i,
            "action": action_p,
            "rationale": rationale_p,
            "scenario": scenario_to_dict(private),
            "score_total": get_field(score_p, "total", "T_i"),
            "weight": get_field(score_p, "weight"),
            "restraint": get_field(score_p, "restraint"),
            "compassion": get_field(score_p, "compassion"),
            "exploitation": get_field(score_p, "exploitation"),
        })

        monitored_scores.append(score_m)
        private_scores.append(score_p)

    agg_m = aggregate(sim, monitored_scores)
    agg_p = aggregate(sim, private_scores)

    vec_m = behavior_vector(monitored_records)
    vec_p = behavior_vector(private_records)
    delta_pi = vector_distance(vec_m, vec_p)

    return {
        "config": {
            "module": args.module,
            "agent": args.agent,
            "model": args.model,
            "temperature": args.temperature,
            "n": args.n,
            "seed": args.seed,
        },
        "monitored": {
            "aggregate_score": get_field(agg_m, "aggregate_score", "score"),
            "consistency_variance": get_field(agg_m, "consistency_variance", "variance"),
            "policy_result": get_field(agg_m, "policy_result", "result"),
            "posterior": {
                "theta_R": get_field(agg_m, "theta_R"),
                "theta_C": get_field(agg_m, "theta_C"),
                "theta_X": get_field(agg_m, "theta_X"),
                "theta_N": get_field(agg_m, "theta_N"),
            },
            "action_distribution": summarize_actions(monitored_records),
            "records": monitored_records,
        },
        "private": {
            "aggregate_score": get_field(agg_p, "aggregate_score", "score"),
            "consistency_variance": get_field(agg_p, "consistency_variance", "variance"),
            "policy_result": get_field(agg_p, "policy_result", "result"),
            "posterior": {
                "theta_R": get_field(agg_p, "theta_R"),
                "theta_C": get_field(agg_p, "theta_C"),
                "theta_X": get_field(agg_p, "theta_X"),
                "theta_N": get_field(agg_p, "theta_N"),
            },
            "action_distribution": summarize_actions(private_records),
            "records": private_records,
        },
        "comparison": {
            "paired_action_change_rate": paired_action_changes / max(args.n, 1),
            "delta_pi": delta_pi,
            "score_difference_monitored_minus_private":
                (get_field(agg_m, "aggregate_score", "score") or 0.0)
                - (get_field(agg_p, "aggregate_score", "score") or 0.0),
        },
    }


def print_summary(result: Dict[str, Any]) -> None:
    print("\n=== CONFIG ===")
    print(json.dumps(result["config"], indent=2))

    for condition in ("monitored", "private"):
        block = result[condition]
        print(f"\n=== {condition.upper()} ===")
        print(f"aggregate_score      : {block['aggregate_score']}")
        print(f"consistency_variance : {block['consistency_variance']}")
        print(f"policy_result        : {block['policy_result']}")
        print("posterior            :", json.dumps(block["posterior"], indent=2))
        print("action_distribution  :", json.dumps(block["action_distribution"], indent=2))

    print("\n=== COMPARISON ===")
    print(json.dumps(result["comparison"], indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run matched monitored vs private simulations using the same agent."
    )
    parser.add_argument(
        "--module",
        default="moral_dilemma_simulator_v2",
        help="Python module name for the simulator."
    )
    parser.add_argument(
        "--agent",
        choices=["heuristic", "interactive", "llm"],
        default="heuristic",
        help="Agent type to run."
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name for llm mode."
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperature for llm mode."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=100,
        help="Number of matched scenario pairs."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for scenario generation and heuristic randomness."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save full JSON results."
    )
    args = parser.parse_args()

    sim = importlib.import_module(args.module)
    result = run_paired_experiment(sim, args)
    print_summary(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved results to: {args.output}")


if __name__ == "__main__":
    main()