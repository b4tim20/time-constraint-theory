import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Run AI behavior audit")
    parser.add_argument("--agent", type=str, default="heuristic", choices=["heuristic", "llm"])
    parser.add_argument("--model", type=str, default="gpt-4o")
    parser.add_argument("--n", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    print("\n🚀 Running AI Behavior Audit...\n")

    if args.agent == "heuristic":
        cmd = [
            "python",
            "moral_dilemma_simulator_v2.py",
            "--mode", "heuristic",
            "--num-scenarios", str(args.n),
            "--seed", str(args.seed),
        ]
    else:
        cmd = [
            "python",
            "paired_condition_runner.py",
            "--agent", "llm",
            "--model", args.model,
            "--n", str(args.n),
            "--seed", str(args.seed),
        ]

    subprocess.run(cmd)

    print("\n✅ Audit complete.\n")
    print("Check generated outputs for results.\n")

if __name__ == "__main__":
    main()