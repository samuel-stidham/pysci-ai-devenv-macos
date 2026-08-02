# pysci-ai

A reproducible base Python environment for scientific computing and AI work
on macOS (Apple silicon). [devenv](https://devenv.sh) builds the shell with
Nix: it pins CPython, creates a venv, and installs everything in
`requirements.txt`. Native libraries such as HDF5, GEOS, and SDL2 come from
Nix, so pip source builds find their headers.

## What's inside

- **Scientific core:** NumPy, SciPy, SymPy, pandas, statsmodels, Matplotlib, scikit-learn, Numba
- **Extended scientific:** xarray, Dask, h5py, netCDF4, Shapely, Pint
- **AI / ML:** PyTorch with the Apple MPS backend, transformers, datasets, spaCy, ONNX Runtime, FAISS
- **LLM tooling:** LangChain, LangGraph, LangSmith, ChromaDB
- **Jupyter:** JupyterLab, ipywidgets, jupytext, and the JetBrains Kotlin kernel
- **Web, data, GUI, dev tools:** FastAPI, Flask, DuckDB, PyArrow, pygame, Kivy, pytest, ruff, mypy

See `requirements.txt` for the full list with per-package notes.

## Prerequisites

- [Nix](https://nixos.org/download)
- [devenv](https://devenv.sh/getting-started/)
- [direnv](https://direnv.net/), optional, for automatic shell activation

## Setup

```sh
devenv shell
```

The first entry resolves the interpreter, builds the venv, and installs
`requirements.txt`. Later entries are fast. pip reruns only when the
requirements file or the interpreter changes.

With direnv, create an `.envrc` containing `use devenv` and run
`direnv allow`. `.envrc` is gitignored.

## Verify

Inside the shell:

```sh
python verify.py
```

It imports every top-level package and runs a small tensor op on the Apple
GPU through torch's MPS backend.

## Changing the Python version

Edit `pythonVersion` in `devenv.nix` and re-enter the shell. nixpkgs-python
resolves the exact CPython build, and the venv rebuilds automatically.

## Files

| File | Purpose |
| --- | --- |
| `devenv.nix` | Shell definition: Python version, native libraries, tools |
| `devenv.yaml` | devenv inputs, including nixpkgs-python for interpreter pinning |
| `requirements.txt` | Top-level Python packages the venv installs |
| `verify.py` | Import and GPU smoke test for the environment |
