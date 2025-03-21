# AssetKit

> A Python toolkit for packaging, discovering, and loading structured runtime assets.

[![PyPI version](https://img.shields.io/pypi/v/assetkit)](https://pypi.org/project/assetkit/)
[![License](https://img.shields.io/pypi/l/assetkit)](https://github.com/docdann/assetkit/blob/main/LICENSE)
[![CI](https://github.com/docdann/assetkit/actions/workflows/ci.yml/badge.svg)](https://github.com/docdann/assetkit/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/docdann/assetkit/branch/main/graph/badge.svg)](https://codecov.io/gh/docdann/assetkit)

---

## 🚀 Features
- Structured asset packaging with a clean `resources/` convention
- Auto-discovery of asset packages via `entry_points`
- Pythonic runtime asset access with `AssetManager`
- CLI scaffolding to create new asset packages

---

## 📦 Installation

```bash
pip install assetkit
```

---

## ⚡ Quick Example

```python
from assetkit.asset_manager import AssetManager

assets = AssetManager(package_root="your_package", resource_dir="resources")
print(assets.list())
print(assets["config/main.yaml"].text())
```

To discover multiple asset packages dynamically:

```python
from assetkit.discovery import discover_asset_managers

packages = discover_asset_managers()
for name, assets in packages.items():
    print(name, assets.list())
```

---

## 🛠 Scaffolding a New Package

```bash
assetkit new myplugin
```

This creates a new Python package with an embedded `resources/` directory and a sample `main.py`.

---

## 📂 Project Structure Example

```
myplugin/
├── pyproject.toml
├── main.py
└── myplugin/
    ├── __init__.py
    └── resources/
        ├── config/
        │   └── main.yaml
        └── images/
            └── test.jpg
```

---

## 🧪 Testing Asset Packages

After installing a package (`pip install ./myplugin`):

```python
from assetkit.discovery import discover_asset_managers
assets = discover_asset_managers()["myplugin"]
print(assets.list())
```

---

## 📄 License

MIT — See [LICENSE](LICENSE)

---

## 📬 More Info

- [GitHub Repository](https://github.com/docdann/assetkit)
- [PyPI Project Page](https://pypi.org/project/assetkit/)