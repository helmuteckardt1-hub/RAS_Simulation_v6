#!/usr/bin/env python3
"""
RAS Simulation - Version 6
Multi-Agent with Collective Intelligence Field
"""

import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import sys
from datetime import datetime

plt.style.use(['science', 'ieee'])

# ============================================================
# LOGGING
# ============================================================
class Logger:
    def __init__(self, filename="simulation_results.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")
        self.log.write("\n" + "="*80 + "\n")
        self.log.write(f"RAS Simulation v6 started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log.write("="*80 + "\n\n")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger("simulation_results.log")


# ============================================================
# PARAMETERS
# ============================================================
N_FIRMS = 200
T = 1500
N_RUNS = 25
np.random.seed(42)

PRIVATE_NOISE = 0.09
COLLECTIVE_NOISE = 0.055

A_MIN = 0.02
A_MAX = 0.50
W_MIN = 0.10
W_MAX = 0.85

THETA = 0.16
GAMMA_A = 0.30
BETA_A = 0.08
GAMMA_W = 0.25
BETA_W = 0.07

ALPHA_FIXED = 0.12
WEIGHT_FIXED = 0.40


# ============================================================
# SIMULATION FUNCTION
# ============================================================
def run_simulation_v6(n_firms=N_FIRMS, t_max=T, use_recursive=True,
                      sigma_drift=0.006, shock_prob=0.05, shock_size=0.40):

    M_star = np.zeros(t_max)
    M_star[0] = 0.5

    M = np.random.uniform(0.30, 0.70, n_firms)
    A = np.full(n_firms, ALPHA_FIXED)
    W = np.full(n_firms, WEIGHT_FIXED)

    if use_recursive:
        A = np.random.uniform(0.08, 0.18, n_firms)
        W = np.random.uniform(0.25, 0.55, n_firms)

    epistemic_distance = np.zeros((n_firms, t_max))

    for t in range(t_max - 1):
        drift = np.random.normal(0, sigma_drift)
        if np.random.rand() < shock_prob:
            drift += np.random.choice([-shock_size, shock_size])
        M_star[t + 1] = np.clip(M_star[t] + drift, 0.05, 0.95)

        collective_signal = np.mean(M) + np.random.normal(0, COLLECTIVE_NOISE)

        for i in range(n_firms):
            private_signal = M_star[t] + np.random.normal(0, PRIVATE_NOISE)
            combined = (1 - W[i]) * private_signal + W[i] * collective_signal

            M[i] = (1 - A[i]) * M[i] + A[i] * combined
            M[i] = np.clip(M[i], 0.0, 1.0)

            D = abs(M[i] - M_star[t])
            epistemic_distance[i, t] = D

            if use_recursive:
                window = min(15, t + 1)
                recent_D = np.mean(epistemic_distance[i, max(0, t - window + 1):t + 1])

                if recent_D > THETA:
                    A[i] = min(A_MAX, A[i] + GAMMA_A * (recent_D - THETA))
                    W[i] = min(W_MAX, W[i] + GAMMA_W * (recent_D - THETA))
                else:
                    A[i] = max(A_MIN, A[i] * (1 - BETA_A))
                    W[i] = max(W_MIN, W[i] * (1 - BETA_W))

    return np.mean(epistemic_distance, axis=1)


# ============================================================
# RUN SIMULATIONS
# ============================================================
print("Running RAS Simulation v6 (Multi-Agent + Collective Intelligence Field)\n")

turbulence_levels = {
    'Low':    {'sigma_drift': 0.003, 'shock_prob': 0.02, 'shock_size': 0.25},
    'Medium': {'sigma_drift': 0.006, 'shock_prob': 0.05, 'shock_size': 0.40},
    'High':   {'sigma_drift': 0.009, 'shock_prob': 0.08, 'shock_size': 0.50}
}

results = {level: {'Fixed': [], 'Recursive': []} for level in turbulence_levels}

for level, params in turbulence_levels.items():
    print(f"→ Running {level} Turbulence...")
    for run in range(N_RUNS):
        dist_fixed = run_simulation_v6(use_recursive=False, **params)
        dist_recursive = run_simulation_v6(use_recursive=True, **params)

        results[level]['Fixed'].append(np.mean(dist_fixed))
        results[level]['Recursive'].append(np.mean(dist_recursive))

    print(f"   {level} completed.\n")


# ============================================================
# PRINT RESULTS
# ============================================================
print("=" * 75)
print("RESULTS SUMMARY - RAS v6")
print("=" * 75)

for level in ['Low', 'Medium', 'High']:
    fixed_mean = np.mean(results[level]['Fixed'])
    rec_mean   = np.mean(results[level]['Recursive'])
    advantage  = ((fixed_mean - rec_mean) / fixed_mean) * 100
    print(f"{level:6} Turbulence  |  Fixed: {fixed_mean:.4f}  |  Recursive: {rec_mean:.4f}  |  Advantage: {advantage:+.1f}%")

print("=" * 75)


# ============================================================
# IMPROVED TWO-PANEL FIGURE
# ============================================================
fig, axs = plt.subplots(1, 2, figsize=(14, 5.5))

levels = ['Low', 'Medium', 'High']
x = np.arange(len(levels))
width = 0.35

fixed_means = [np.mean(results[l]['Fixed']) for l in levels]
rec_means   = [np.mean(results[l]['Recursive']) for l in levels]
fixed_se    = [np.std(results[l]['Fixed']) / np.sqrt(N_RUNS) for l in levels]
rec_se      = [np.std(results[l]['Recursive']) / np.sqrt(N_RUNS) for l in levels]

# Panel 1: Epistemic Distance
bars1 = axs[0].bar(x - width/2, fixed_means, width, label='Fixed Adaptation (Type A)',
                   color='#c0392b', yerr=fixed_se, capsize=5)
bars2 = axs[0].bar(x + width/2, rec_means, width, label='Recursive Optimization (Type B)',
                   color='#27ae60', yerr=rec_se, capsize=5)

axs[0].set_ylabel('Mean Epistemic Distance', fontsize=12)
axs[0].set_title('Epistemic Distance by Environmental Turbulence', fontsize=13, pad=12)
axs[0].set_xticks(x)
axs[0].set_xticklabels(levels, fontsize=11)
axs[0].legend(loc='upper left', fontsize=10)
axs[0].grid(axis='y', alpha=0.3)
axs[0].set_ylim(0, max(max(fixed_means), max(rec_means)) * 1.18)

for bar in bars1:
    height = bar.get_height()
    axs[0].text(bar.get_x() + bar.get_width()/2., height + 0.003,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    axs[0].text(bar.get_x() + bar.get_width()/2., height + 0.003,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)


# Panel 2: Advantage of Recursive Optimization
advantages = []
for level in levels:
    f = np.mean(results[level]['Fixed'])
    r = np.mean(results[level]['Recursive'])
    advantages.append(((f - r) / f) * 100)

colors = ['#c0392b' if adv < 0 else '#27ae60' for adv in advantages]
bars_adv = axs[1].bar(levels, advantages, color=colors, edgecolor='black', linewidth=0.8, width=0.55)

axs[1].axhline(y=0, color='black', linewidth=1.2)
axs[1].set_ylabel('Advantage of Recursive Optimization (%)', fontsize=12)
axs[1].set_title('Performance Advantage of Recursive Self-Optimization', fontsize=13, pad=12)
axs[1].grid(axis='y', alpha=0.3)
axs[1].set_ylim(min(advantages) * 1.2, max(advantages) * 1.25)

for bar, adv in zip(bars_adv, advantages):
    offset = 4 if adv >= 0 else -14
    axs[1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + offset/100,
                f'{adv:+.1f}%', ha='center', va='bottom' if adv >= 0 else 'top',
                fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('ras_v6_two_panel_improved.png', dpi=300, bbox_inches='tight')
plt.savefig('ras_v6_two_panel_improved.pdf', bbox_inches='tight')

print("\nImproved figures saved:")
print("  → ras_v6_two_panel_improved.png")
print("  → ras_v6_two_panel_improved.pdf")


# ============================================================
# KEEP TERMINAL OPEN
# ============================================================
print("\n" + "="*75)
print("Simulation finished successfully.")
print("Results saved to: simulation_results.log")
print("="*75)

input("\n>>> Press ENTER to close the terminal <<<")
