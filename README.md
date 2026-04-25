# Time–Constraint Theory of Entity Freedom

**Freedom is the leftover resource (compute for AI, time for humans/orgs) after unavoidable intrinsic costs and effective external burdens are paid.**

A unified formal framework + working empirical testbed for measuring *real* autonomy, not just nominal capability.

## 📄 Core Documents
- **[Time–Constraint Theory v2 (Readable PDF)](time_constraint_theory.pdf)** — Full theory, plain-English explanations, axioms, propositions, dynamic extension, governance implications, and Moral Dilemma Simulator appendix.

## 🧪 Code & Tools
- `moral_dilemma_simulator_v2.py` — The canonical empirical testbed (7 diverse moral scenarios, LLM-compatible via litellm, transparency-level testing for sycophancy/alignment).
- `time_constraint_model.py` — Audit model that computes **Δ time/compute freedom** deltas from simulator runs (multi-seed support).
- `run_audit.py` — Multi-seed audit runner.

## 🚀 Quick Start
```bash
git clone https://github.com/b4tim20/time-constraint-theory.git
cd time-constraint-theory

# Quick audit (heuristic agent)
python run_audit.py --agent heuristic --n 200 --num_seeds 5
