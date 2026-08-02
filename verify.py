#!/usr/bin/env python3
"""Verify pysci-ai environment: import every top-level package, report GPU status.

CLI-only dev tools (black, ruff, mypy, pytest, pre-commit, build, twine, ipdb)
are installed by requirements.txt but not import-checked here. Some, like ruff,
ship no importable module, so a failed import would be a false negative. This
script verifies libraries you actually import in code, plus live access to the
Apple GPU through torch's MPS (Metal) backend.
"""

import sys
import importlib

PACKAGES = {
    "Scientific core": [
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("sympy", "sympy"),
        ("mpmath", "mpmath"),
        ("gmpy2", "gmpy2"),
        ("pandas", "pandas"),
        ("statsmodels", "statsmodels"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("sklearn", "scikit-learn"),
        ("numba", "numba"),
        ("Cython", "cython"),
        ("networkx", "networkx"),
        ("contourpy", "contourpy"),
        ("PIL", "pillow"),
    ],
    "Extended scientific": [
        ("xarray", "xarray"),
        ("dask", "dask"),
        ("h5py", "h5py"),
        ("netCDF4", "netcdf4"),
        ("pint", "pint"),
        ("uncertainties", "uncertainties"),
        ("shapely", "shapely"),
        ("symengine", "symengine"),
    ],
    "Visualization": [
        ("plotly", "plotly"),
        ("bokeh", "bokeh"),
        ("altair", "altair"),
    ],
    "Data": [
        ("duckdb", "duckdb"),
        ("pyarrow", "pyarrow"),
        ("sqlalchemy", "sqlalchemy"),
    ],
    "Jupyter": [
        ("jupyterlab", "jupyterlab"),
        ("ipywidgets", "ipywidgets"),
        ("jupytext", "jupytext"),
    ],
    "AI / ML": [
        ("torch", "pytorch"),
        ("torchvision", "torchvision"),
        ("torchaudio", "torchaudio"),
        ("transformers", "transformers"),
        ("accelerate", "accelerate"),
        ("safetensors", "safetensors"),
        ("tokenizers", "tokenizers"),
        ("datasets", "datasets"),
        ("huggingface_hub", "huggingface-hub"),
        ("spacy", "spacy"),
        ("nltk", "nltk"),
        ("sentencepiece", "sentencepiece"),
        ("onnxruntime", "onnxruntime"),
        ("faiss", "faiss-cpu"),
    ],
    "LLM tooling": [
        ("langchain", "langchain"),
        ("langgraph", "langgraph"),
        ("langsmith", "langsmith"),
        ("chromadb", "chromadb"),
    ],
    "Web / API": [
        ("flask", "flask"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("bs4", "beautifulsoup4"),
        ("httpx", "httpx"),
        ("aiohttp", "aiohttp"),
    ],
    "GUI / media": [
        ("pygame", "pygame"),
        ("kivy", "kivy"),
    ],
    "Dev tools": [
        ("pydantic", "pydantic"),
        ("pybind11", "pybind11"),
        ("rich", "rich"),
    ],
}


def main():
    print(f"Python {sys.version}\n")

    passed = 0
    failed = 0
    failures = []

    for section, packages in PACKAGES.items():
        print(f"── {section} ──")
        for module_name, pip_name in packages:
            try:
                importlib.import_module(module_name)
                print(f"  ✓ {pip_name}")
                passed += 1
            except ImportError as e:
                print(f"  ✗ {pip_name}: {e}")
                failed += 1
                failures.append(pip_name)
        print()

    # GPU status. A tiny tensor op runs on the mps device because
    # availability alone does not prove the backend can execute kernels.
    print("── GPU (MPS / Apple Metal) ──")
    try:
        import torch

        if torch.backends.mps.is_available():
            x = (torch.ones(8, device="mps") * 2).sum().item()
            print("  ✓ MPS available")
            print(f"  ✓ smoke test: computed {x:.0f} on mps device")
        else:
            print("  ✗ MPS not available to PyTorch")
    except ImportError:
        print("  ✗ PyTorch not installed, skipping GPU check")

    print()
    print(f"Result: {passed} passed, {failed} failed")
    if failures:
        print(f"Failed: {', '.join(failures)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
