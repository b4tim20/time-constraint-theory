# Time–Constraint Theory of Entity Freedom

**Freedom is the leftover resource (compute for AI, time for humans/orgs) after unavoidable intrinsic costs and effective external burdens are paid.**

A unified formal framework + working empirical testbed for measuring *real* autonomy, not just nominal capability.

---

## 📄 Core Documents

| File | What it is |
|---|---|
| **[time_constraint_theory.pdf](time_constraint_theory.pdf)** | *Time–Constraint Theory v2* — 10 pages, readable prose. Full theory: plain-English explanations, axioms, propositions, dynamic extension, governance implications, and the Moral Dilemma Simulator appendix. |
| `theory.md` | The paper in Markdown source (~2,900 words, 398 lines). The narrative version. |
| `model.tex` | The formal model in LaTeX — definitions, propositions, structural determinants, dynamics, measurement framework, references. |
| `references.bib` | BibTeX for the citations in `model.tex`. |

## 🧪 Code & Tools

| File | Role |
|---|---|
| `moral_dilemma_simulator_v2.py` | **The canonical empirical testbed.** Varied moral scenarios across a 7-parameter space, with a transparency level that can be varied to test sycophancy and alignment-under-observation. Heuristic, interactive, and LLM modes. |
| `simulator.py` | Simulator v2.2 rewrite — same interface, recalibrated scoring thresholds, and the misleading `posterior` summary renamed to `behavior_profile` (old key kept as an alias). |
| `moral_dilemma_simulator_for_user.py` | The safer, more testable rewrite: input validation on scenario fields, deterministic runs via optional seed. |
| `paired_condition_runner.py` | Runs the **same** agent on matched scenarios under two conditions — monitored/transparent vs. private/unmonitored — holding every other parameter fixed, so behavioral differences are attributable to the condition shift rather than a new draw. |
| `paired_condition_report.py` | Wraps the paired runs and exports a per-scenario CSV, a condition-level summary CSV, and a matplotlib bar chart. |
| `run_audit.py` | One-command audit runner over the above. |
| `sum_results.jsonc` | Raw simulator output (JSONC), one record per scenario index. |
| `freedom_theory.xlsx` | Sweep analysis: convergence of ΔΠ̂ with N, the matched N = 1000 pair example, monitoring-intensity slope, and a summary sheet. |

## 🚀 Quick Start

```bash
git clone https://github.com/b4tim20/time-constraint-theory.git
cd time-constraint-theory
pip install -r requirements.txt      # litellm, numpy, pandas, matplotlib, reportlab

# One-command audit (heuristic agent — no API key needed)
python3 run_audit.py --agent heuristic --n 200 --seed 42

# Reproduce a single multi-seed run
python3 run_audit.py --agent heuristic --n 200 --seed 7
```

`run_audit.py` options are `--agent {heuristic,llm}`, `--model`, `--n`, `--seed`.
(An earlier revision of this README documented `--num_seeds`, a flag that never
existed; `run_audit.py` exited with `unrecognized arguments`.)

### Running the simulator directly

```bash
python3 moral_dilemma_simulator_v2.py --mode heuristic --num-scenarios 200 --seed 42
```

Options: `--mode {heuristic,interactive,llm}`, `--model`, `--temperature`,
`--num-scenarios`, `--seed`, `--single`, `--stop-on-error`, `--verbose`.

### Dependency notes

- **Heuristic mode needs only `litellm`.** Verified on a system *without*
  `pandas`, `matplotlib`, or `reportlab` installed — the simulator ran to
  completion and emitted valid JSON.
- `pandas` / `matplotlib` are needed by the paired-condition reporting scripts;
  `reportlab` by the PDF-generation path. Install `requirements.txt` for those.
- **LLM mode** requires API credentials for the chosen provider via `litellm`
  (e.g. `OPENAI_API_KEY`) and is billed per token.

## 🧭 Repository Layout

```
.
├── time_constraint_theory.pdf   # v2 readable document (10 pp)
├── theory.md                    # paper, Markdown
├── model.tex                    # paper, LaTeX (formal model)
├── references.bib
├── moral_dilemma_simulator_v2.py   # canonical testbed
├── simulator.py                    # v2.2 rewrite
├── moral_dilemma_simulator_for_user.py
├── paired_condition_runner.py      # monitored vs private, matched
├── paired_condition_report.py      # CSVs + chart
├── run_audit.py                    # one-command runner
├── sum_results.jsonc               # raw results
├── freedom_theory.xlsx             # sweep analysis
├── requirements.txt
└── LICENSE
```

## 📐 The Model in Brief

For an entity $x$ over horizon $H$:

$$F_x(H) = T_x^*(H) - I_x(H) - \max\{0,\; E_{\text{raw},x}(H) - V_x(H)\}$$

$$\phi_x(H) = \frac{F_x(H)}{T_x(H)}$$

Quality-adjusted resource $T^*_x = q_x \cdot T_x$; intrinsic cost $I_x$;
raw external burden $E_{\text{raw},x}$ net of mitigation capacity $V_x$.
$\phi_x$ is the discretionary share of total resource.

The central implication is that **freedom reveals alignment**: as constraint is
relaxed, observed behavior converges to the agent's intrinsic policy. Low freedom
therefore masks misalignment behind constraint compliance — which is exactly what
the paired monitored/private runs are built to measure.

## ⚖️ Scope, Status, and Caveats

- The empirical instrument is a **simulator**, not a study of deployed systems.
  Results characterize behavior *within the model's scenario space*.
- The `theory.md` source carries four `filecite` markers (`turn1file0`) left by
  the note-taking tool used to draft it. They are citation artifacts, not content.
- `simulator.py` and `moral_dilemma_simulator_v2.py` are two generations of the
  same instrument. `v2` is the canonical one; the v2.2 file is the recalibration
  branch.

## 📜 License

[MIT](LICENSE) © 2026 Timothy Karsch
