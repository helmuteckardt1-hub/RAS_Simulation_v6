# RAS_Simulation_v6

Multi-agent simulation of the **Recursive Adaptive System (RAS)** for studying organizational adaptation in competitive, non-stationary environments.

This repository accompanies the paper:  
**"A Recursive Framework for the Market Epistemic Field and Collective Intelligence in Competitive Systems"**

## Overview

The simulation models firms as adaptive agents that maintain internal representations of a moving market state (proxy for the Idealized Market Epistemic Field). Each firm receives noisy private and collective signals and updates its internal model accordingly.

Two types of agents are compared:
- **Type A (Fixed Adaptation)**: Agents use constant adaptation parameters.
- **Type B (Recursive Self-Optimization)**: Agents can adjust their adaptation rate and reliance on collective information based on recent performance.

The model examines how recursive self-optimization affects epistemic distance and performance under different levels of environmental turbulence.

## Features

- Heterogeneous multi-agent environment
- Private and collective (CIF-based) information signals
- Recursive self-optimization mechanism
- Configurable environmental turbulence (drift + shocks)
- Batch runs with statistical output

## Requirements

- Python 3.8+
- NumPy
- Matplotlib (for visualization)

Install dependencies:

```bash
pip install numpy matplotlib
