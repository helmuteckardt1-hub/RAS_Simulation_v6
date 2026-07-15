# RAS_Simulation_v6

Multi-agent simulation of the **Recursive Adaptive System (RAS)**. Compares agents using fixed adaptation rules against agents capable of recursive self-optimization under varying levels of environmental turbulence.

This code accompanies the paper:  
**"A Recursive Framework for the Market Epistemic Field and Collective Intelligence in Competitive Systems"**

## Overview

The simulation models firms as adaptive agents maintaining internal representations of a moving market state. Each agent receives noisy private and collective signals (representing the Collective Intelligence Field) and updates its beliefs accordingly.

Two agent types are compared:
- **Type A (Fixed Adaptation)**: Uses constant adaptation parameters.
- **Type B (Recursive Self-Optimization)**: Dynamically adjusts adaptation rate and reliance on collective information based on recent performance.

## Requirements

Install the required packages using:

```bash
pip install -r requirements.txt
