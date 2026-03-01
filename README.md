# DSSAT Dürnast Project

End-to-end crop modeling workflows for the **Dürnast** long-term experiment (Freising, Bayern, Germany), using **DSSAT** (Decision Support System for Agrotechnology Transfer) with the **N-Wheat** model. The project supports both **Spring Wheat** (e.g. 2015) and **Winter Wheat** (e.g. 2017) nitrogen response trials.

---

## Overview

This repository contains **two main pipelines** that work together:

| Pipeline | Role | Stack |
|----------|------|--------|
| **csmTools_durnast** | Data ETL: raw → ICASA → DSSAT inputs | R (csmTools + duernast_exp_modeling) |
| **DSSAT_Durnast** | Run DSSAT, post-process, visualize, evaluate | Python + DSSAT CSM (DSCSM048) |

- **csmTools_durnast** prepares experiment data (BonaRes, soil, weather) and writes DSSAT-ready files.
- **DSSAT_Durnast** runs N-Wheat simulations, generates 12-panel visualizations, model evaluation metrics, and optional water-sensitivity analysis.

---

## Repository Layout (Top Level)

```
DSSAT_Durnast/                    ← You are here (project root)
├── README.md                     ← This file
├── STRUCTURE_OVERVIEW.md         ← Folder-by-folder structure of both pipelines
├── csmTools_durnast/             ← R ETL pipeline (data prep → DSSAT inputs)
│   ├── csmTools-main/            ← csmTools R package
│   └── duernast_exp_modeling-main/   ← Dürnast-specific mapping & build
└── DSSAT_Durnast /               ← Python simulation & analysis pipeline
    ├── GENERALIZED_PIPELINE/     ← Master workflow, config, viz, evaluation
    ├── DUERNAST2015/             ← 2015 experiment (Spring Wheat)
    ├── DUERNAST2017/             ← 2017 experiment (Winter Wheat)
    ├── water_sensitivity analysis results/
    ├── Weather data extraction from NASAPOWER/
    ├── DSSAT48/                  ← (not in repo) Install from https://dssat.net
    ├── run_2015.bat / run_2017.bat
    └── ...
```

See **STRUCTURE_OVERVIEW.md** for a detailed structure of each pipeline and folder.

---

## Pipeline 1: csmTools_durnast (R — Data ETL)

**Purpose:** Turn raw and external data into ICASA- and DSSAT-ready inputs for the Dürnast experiment.

**Main steps:**
1. Read raw experiment data and BonaRes metadata.
2. Map to **ICASA** (convert_dataset: `bonares-lte_de` → `icasa`).
3. Attach soil from SoilGrids (e.g. `get_soil_profile`).
4. Map to **DSSAT** (convert_dataset: `icasa` → `dssat`).
5. Write ICASA CSVs to `data/1_icasa/` and DSSAT input files to `data/2_dssat/`.

**Entry point:**  
- R script: `duernast_exp_modeling-main/R/lte_duernast_data_mapping.R`  
- Depends on **csmTools** (from `csmTools-main/` or GitHub).

**Outputs:**  
- `duernast_exp_modeling-main/data/1_icasa/*.csv`  
- `duernast_exp_modeling-main/data/2_dssat/*` (DSSAT experiment/weather/soil files)

---

## Pipeline 2: DSSAT_Durnast (Python — Simulation & Analysis)

**Purpose:** Run DSSAT N-Wheat for Dürnast 2015/2017, then visualize and evaluate results.

**Main steps:**
1. **Prerequisites** — Check experiment dir, input files, Python deps.
2. **DSSAT run** — Copy inputs to `output/`, run `DSCSM048.EXE`, write Summary/PlantGro/Weather/Soil etc.
3. **Visualization** — 12-panel figures (seasonal progression, stress, yield, validation) for selected treatments (e.g. 1, 8, 15).
4. **Model evaluation** — Metrics (e.g. RMSE, R², MAE) and comparison plots for all 15 treatments.
5. **Summary** — List generated outputs and workflow status.

**Entry points:**
- **Master workflow:**  
  `DSSAT_Durnast /GENERALIZED_PIPELINE/MASTER_WORKFLOW.py`  
  - `python MASTER_WORKFLOW.py 2015` — 2015 only  
  - `python MASTER_WORKFLOW.py 2017` — 2017 only  
  - `python MASTER_WORKFLOW.py --all` — both  
  - `python MASTER_WORKFLOW.py --list` — list experiments
- **Convenience:**  
  `run_2015.bat` / `run_2017.bat` (call MASTER_WORKFLOW with 2015 or 2017).

**Config:**  
`GENERALIZED_PIPELINE/config.py` — experiment year, file prefixes, multi-year and normalization flags.

**Outputs (per experiment):**
- `DUERNAST2015/output/` or `DUERNAST2017/output/`:  
  Summary.OUT, PlantGro.OUT, PlantN.OUT, SoilWat.OUT, Weather.OUT, etc.
- `output/<prefix>_comprehensive_analysis.png|pdf`
- `output/Model_analysis/<prefix>_comparison_all_treatments.csv`, `_model_metrics_summary.csv`, `_model_evaluation.png|pdf`

**Extras:**
- **Water sensitivity:**  
  `water_sensitivity analysis results/` — scripts and CSV for % observed yield vs extra rainfall (Spring vs Winter).
- **Weather:**  
  `Weather data extraction from NASAPOWER/` — e.g. `retrieve_nasa_power_weather_data.py` for supplementary weather.

---

## Requirements

- **Pipeline 1 (R):** R, csmTools (and its dependencies), packages used in `lte_duernast_data_mapping.R` (e.g. dplyr, openxlsx2, sf). BonaRes metadata URL and optional SoilGrids access.
- **Pipeline 2 (Python):** Python 3, pandas, numpy, matplotlib, seaborn (see `GENERALIZED_PIPELINE/requirements.txt`). **DSSAT** must be installed separately (e.g. `DSSAT48` with `DSCSM048.EXE`, Genotype files) from [dssat.net](https://dssat.net); the `DSSAT48/` folder is not stored in this repo. For full workflow, run from `DSSAT_Durnast /` so paths to `GENERALIZED_PIPELINE` and experiment dirs resolve.

---

## Quick Start (Simulation & Analysis Only)

From the **DSSAT_Durnast ** directory (or project root, depending on how paths are set):

```bash
# Run 2015 (Spring Wheat) full workflow
python GENERALIZED_PIPELINE/MASTER_WORKFLOW.py 2015

# Run 2017 (Winter Wheat) full workflow
python GENERALIZED_PIPELINE/MASTER_WORKFLOW.py 2017

# Or use batch files (Windows)
run_2015.bat
run_2017.bat
```

Ensure DSSAT is installed and that `DUERNAST2015/input/` and `DUERNAST2017/input/` contain the required `.WHX`, `.WTH`, `.WHA`, `.WHT`, `DE.SOL` and Genotype files as expected by the master workflow.

---

## Data Flow (Conceptual)

```
Raw / BonaRes / SoilGrids
         ↓
   [csmTools_durnast]
   R: convert_dataset, get_soil_profile, build_simulation_files
         ↓
   data/1_icasa/*.csv, data/2_dssat/*
         ↓
   (Optional: copy/move DSSAT inputs into DSSAT_Durnast experiment input folders)
         ↓
   [DSSAT_Durnast — GENERALIZED_PIPELINE]
   Python: MASTER_WORKFLOW → DSSAT run → create_duernast_visualizations → model_evaluation_analysis
         ↓
   output/*.OUT, *comprehensive_analysis*, Model_analysis/*.csv, *.png, *.pdf
```

---

## References

- **DSSAT:** https://dssat.net  
- **csmTools:** FAIRagro UC6; ETL and ICASA/DSSAT mapping (see `csmTools_durnast/csmTools-main/README.md`)  
- **ICASA:** [ICASA data dictionary](https://github.com/DSSAT/ICASA-Dictionary)  
- **Dürnast:** Long-term experiment, TUM, Dürnast (Freising), Germany.
