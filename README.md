# AInventory — Demand Forecasting & Inventory Policies

Platform for forecasting demand and calculating inventory policies.
- Models: Prophet, SARIMA, ML baselines
- UI: Streamlit
- Processes: SemVer, trunk-based, pre-commit, CI

## Quick Start
python -m venv .venv && source .venv/bin/activate
pip install -U pip -r requirements.txt
pre-commit install
make app

## Data Contracts
See docs/data_contracts.md
