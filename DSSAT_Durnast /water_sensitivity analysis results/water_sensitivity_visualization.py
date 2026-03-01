#!/usr/bin/env python3
"""
Water Sensitivity: % of observed yield vs extra rainfall.
Shows how close simulated yield is to observed (100% = optimum).
Reads input from sensitivity_table_percent_observed.csv in this folder.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# Path to table (same folder as this script)
SCRIPT_DIR = Path(__file__).resolve().parent
TABLE_PATH = SCRIPT_DIR / "sensitivity_table_percent_observed.csv"

# Plot style by treatment
group_style = {
    'Control (0N)':     {'color': '#2E7D32', 'marker': 'o'},
    'Low N (120N)':     {'color': '#F9A825', 'marker': 's'},
    'High N (180N)':    {'color': '#C62828', 'marker': '^'},
}

# CSV column names -> display name
COL_TO_LABEL = {
    'Spring_Control_0N': 'Control (0N)',
    'Spring_Low_N_120N': 'Low N (120N)',
    'Spring_High_N_180N': 'High N (180N)',
    'Winter_Control_0N': 'Control (0N)',
    'Winter_Low_N_120N': 'Low N (120N)',
    'Winter_High_N_180N': 'High N (180N)',
}


def load_sensitivity_table():
    """Load % observed yield from CSV; returns (x, spring_pct, winter_pct)."""
    if not TABLE_PATH.exists():
        raise FileNotFoundError(f"Sensitivity table not found: {TABLE_PATH}")
    df = pd.read_csv(TABLE_PATH)
    x = np.array(df["weekly_rain_mm"], dtype=float)
    spring_pct = {
        COL_TO_LABEL["Spring_Control_0N"]: list(df["Spring_Control_0N"]),
        COL_TO_LABEL["Spring_Low_N_120N"]: list(df["Spring_Low_N_120N"]),
        COL_TO_LABEL["Spring_High_N_180N"]: list(df["Spring_High_N_180N"]),
    }
    winter_pct = {
        COL_TO_LABEL["Winter_Control_0N"]: list(df["Winter_Control_0N"]),
        COL_TO_LABEL["Winter_Low_N_120N"]: list(df["Winter_Low_N_120N"]),
        COL_TO_LABEL["Winter_High_N_180N"]: list(df["Winter_High_N_180N"]),
    }
    return x, spring_pct, winter_pct


def main():
    x, spring_pct, winter_pct = load_sensitivity_table()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

    # 100% = optimum (target line)
    for ax in (ax1, ax2):
        ax.axhline(100, color='#333333', linestyle='-', linewidth=1.5, alpha=0.9, label='100% (observed)')
        ax.fill_between([-0.5, 20.5], 99, 101, color='gray', alpha=0.15)

    # ---- Panel A: Spring Wheat 2015 ----
    for trt, style in group_style.items():
        ax1.plot(x, spring_pct[trt], marker=style['marker'], color=style['color'], linewidth=2,
                 markersize=8, label=trt)
    ax1.set_xlabel('Extra weekly rainfall (mm/week)', fontsize=11)
    ax1.set_ylabel('% of observed yield', fontsize=11)
    ax1.set_title('a) Spring Wheat (2015)', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'{v}\n(+{v*7} mm)' for v in x])
    ax1.legend(loc='lower right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_axisbelow(True)
    ax1.set_ylim(75, 120)
    ax1.set_xlim(-0.5, 20.5)

    # ---- Panel B: Winter Wheat 2017 ----
    for trt, style in group_style.items():
        ax2.plot(x, winter_pct[trt], marker=style['marker'], color=style['color'], linewidth=2,
                 markersize=8, label=trt)
    ax2.set_xlabel('Extra weekly rainfall (mm/week)', fontsize=11)
    ax2.set_ylabel('% of observed yield', fontsize=11)
    ax2.set_title('b) Winter Wheat (2017)', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{v}\n(+{v*7} mm)' for v in x])
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.set_ylim(75, 120)
    ax2.set_xlim(-0.5, 20.5)

    fig.suptitle('Water sensitivity: simulated yield as % of observed (100% = optimum)', fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()

    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / 'water_sensitivity_percent_observed.png'
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


if __name__ == '__main__':
    main()
