# AssetKit MVP — Usage Guide

This document explains how to install, use, and test the AssetKit MVP framework.

---

## ✅ Step 1: Install AssetKit SDK
Navigate to the `assetkit_mvp` directory and install it in editable mode:

```bash
cd assetkit_mvp
pip install -e .
```

---

## ✅ Step 2: Scaffold a New Asset Package
Use the CLI to generate a new package:

```bash
assetkit new myplugin
```

This will create:

```
myplugin/
├── pyproject.toml
└── myplugin/
    ├── __init__.py
    └── resources/
```

---

## ✅ Step 3: Add Assets
Populate `myplugin/resources/` with your structured files:

Example structure:
```
myplugin/
└── myplugin/
    └── resources/
        ├── config/
        │   └── main.yaml
        ├── templates/
        │   └── base.tpl
```

---

## ✅ Step 4: Install the Asset Package

```bash
cd myplugin
pip install .
```

---

## ✅ Step 5: Discover and Use Assets

Create a test script `try_assets.py`:
```python
from assetkit.discovery import discover_asset_managers

assets_by_package = discover_asset_managers()

for pkg, assets in assets_by_package.items():
    print(f"Package: {pkg}")
    print("Assets:", assets.list())

    if "config/main.yaml" in assets:
        print("YAML content:\n", assets["config/main.yaml"].text())
```

Run it:
```bash
python try_assets.py
```

---

## ✅ Step 6: Package and Distribute (Optional)

```bash
cd myplugin
python -m build
twine upload dist/*
```

This allows other users to install your asset package via pip.

---

## You're ready to go 🎉
Use AssetKit to modularize and manage structured asset content in Python cleanly and scalably.
