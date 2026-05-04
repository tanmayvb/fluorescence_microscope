# Fluorescence ND2 Analysis Pipeline

## Overview

This project provides a streamlined pipeline for working with **fluorescence microscopy ND2 files**.
It is designed to handle large time-series datasets efficiently and produce meaningful visualizations such as intensity evolution over time and frame-based plots.

The internal codebase manages:

* ND2 file loading
* Memory-efficient processing
* Intensity extraction
* Visualization

Users only need to **install dependencies and run the main script**.

---

## Getting Started

### 1. Clone the Repository

```bash

git clone https://github.com/<yourname>/<repo-name>.git
cd <repo-name>

```
---

## Installation

### Using pip

```bash
pip install nd2 tifffile numpy matplotlib scipy dask
```
---

### Using `uv` (recommended)

If you are using `uv`:

```bash
uv sync
```

---

### Windows Notes

* Use **PowerShell** or **Anaconda Prompt**
* Ensure Python ≥ 3.9 is installed
* If `uv` is not available:

  ```bash
  pip install uv
  ```

---

## How to Run

The project is designed with a **single entry point**.

```bash
uv run python src/fluorescence_loader/plot_intensity.py --file_path /Users/tanmay/LenevoINFN/Work/BratatiImageJ/InFile/nd005.nd2
```

---

## What the Script Does

Running the main script will automatically:

* Load the ND2 fluorescence dataset
* Process time-series frames efficiently
* Compute intensity evolution
* Generate plots (intensity vs time, sampled frames, etc.)<br>

No manual configuration of internal modules is required.

---

## Input Data

Place your ND2 file inside:

```text
data/
```

Update the "file path" inside the project.

---

## Outputs

Results plots: You can save accoring to choice,  
next we will fix the plots will be saved automatically in some folder and then don't need to worry


---

## Notes

* ND2 files can be large → the pipeline uses **lazy loading** to avoid memory issues
* Some ND2 files may not include timestamps → time is inferred from frame index
* Visualization uses **contrast scaling** for fluorescence data

---

## Requirements Summary

* nd2
* tifffile
* numpy
* matplotlib
* scipy
* dask

---

## Troubleshooting

### Module not found (`nd2`)

```bash
pip install nd2
```

---

### Environment issues

Ensure dependencies are installed in the active environment:

```bash
pip list
```

---

### Large file performance

* Close other applications
* Prefer using `uv` or virtual environments

---

## Summary

This project provides a **ready-to-run pipeline** for fluorescence ND2 data:

✔ Minimal setup
✔ Single command execution
✔ Scalable for large datasets
✔ Extendable for advanced analysis

---

## Future Extensions

* ROI-based analysis
* ΔF/F normalization
* Kymograph generation
* ML-based feature extraction

---



