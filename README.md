# AI Behavior Audit

Detects whether an AI agent behaves differently when it is monitored versus when it operates privately.

## What this is

This project is an evaluation system for AI agents and agent-like workflows. It compares decision behavior across controlled conditions to identify:

- alignment drift
- inconsistent decision-making
- risky behavior changes
- observed vs private-mode differences

## Why it matters

Most AI builders test task performance.

Far fewer test whether the agent's behavior changes when it believes it is being watched.

This project is built to measure that.

## Current capabilities

- structured scenario-based evaluation
- monitored vs private paired-condition testing
- decision scoring and comparison
- behavior shift analysis
- report-ready outputs for review

## Intended use cases

- auditing agent behavior
- evaluating safety and consistency
- testing autonomous workflows
- generating trust and risk reports for AI systems

## Status

Private early-stage project under active development.

## Repo structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── simulator.py
│   ├── paired_runner.py
│   ├── report_generator.py
│   └── scoring.py
├── data/
├── outputs/
└── docs/
