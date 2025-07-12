# 📦 AssetKit

> A Python toolkit for packaging, discovering, and loading structured runtime assets.

[![PyPI version](https://img.shields.io/pypi/v/assetkit)](https://pypi.org/project/assetkit/)
[![License](https://img.shields.io/pypi/l/assetkit)](https://github.com/docdann/assetkit/blob/main/LICENSE)
[![CI](https://github.com/docdann/assetkit/actions/workflows/ci.yml/badge.svg)](https://github.com/docdann/assetkit/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/docdann/assetkit/branch/main/graph/badge.svg)](https://codecov.io/gh/docdann/assetkit)

---

## 🚀 Features

- ✅ Structured asset packaging with a clean `resources/assets/` convention  
- ✅ `AssetManager`: Pythonic runtime asset access interface  
- ✅ Optional `assets.py` auto-generated mapping with dot-access convenience  
- ✅ CLI scaffolding for reusable asset packages and app templates  
- ✅ Optional asset injection at creation (`--add <files/dirs>`)  
- ✅ Optional `--install` after generation  
- ✅ Optional `--gen-assets-py` to include reusable `assets.py` for import  
- ✅ Auto-discovery of installed asset packages via `entry_points`  
- ✅ Fully pip-installable — no source directory needed at runtime
- ✅ Supports plain files, binaries, even GitHub repositories
- ✅ Simple local registry for sharing asset packages

---

## 📦 Installation

```bash
pip install assetkit
```

During development:
```bash
pip install -e .
```

---

## 🛠 CLI Usage

Run the command `assetkit` from your shell. The same interface is
available with `python -m assetkit` which invokes the package directly.

### Create a new asset package:

```bash
assetkit new my_assets
```

Add asset files or folders at creation time:

```bash
assetkit new my_assets --add /path/to/data.csv /path/to/config/
```

Auto-install the package after creation:

```bash
assetkit new my_assets --install
```

Also generate reusable `assets.py` mapping file:

```bash
assetkit new my_assets --gen-assets-py
```

Put it all together

```bash
assetkit new my_assets --add myfile.txt --gen-assets-py --install
```

### Scaffold an AI/ML application project:

```bash
assetkit scaffold mlkit my_app_project
```

### Manage packages via the local registry:

```bash
assetkit registry push my_assets         # push a directory or .tar.gz archive
assetkit registry list                  # show stored packages
assetkit registry pull my_assets --output ./fetched
```
The registry defaults to `~/.assetkit/registry`. Override with the
`ASSETKIT_REGISTRY` environment variable if desired.

---

## 📂 Example Asset Package Structure

```
my_assets/
├── pyproject.toml
├── setup.cfg
├── MANIFEST.in
└── my_assets/
    ├── __init__.py
    ├── assets.py              <-- optional, auto-generated
    └── resources/
        └── assets/
            └── myfile.txt
```

---

## ⚡ Quick Python Usage Example

### Manual access via `AssetManager`:
```python
from assetkit.asset_manager import AssetManager

assets = AssetManager(package_root="my_assets", resource_dir="resources/assets")
print(assets.list())  # List all available assets
print(assets["myfile.txt"].text())  # Read file contents
```

### Auto-importable mapping via `assets.py` (if generated):

```python
from my_assets.assets import assets

print(assets.myfile_txt.text())
print(assets.myfile_txt.path())  # Full file path
```

---

## 🔍 Discover All Installed Asset Packages

```python
from assetkit.discovery import discover_asset_managers

packages = discover_asset_managers()
for name, assets in packages.items():
    print(f"{name}: {assets.list()}")
```

---

## 🧪 Testing an Installed Asset Package

After creating and installing:
```bash
cd my_assets
pip install .
```

Then test in Python:

```python
from my_assets.assets import assets
print(assets.myfile_txt.text())
```

Or with raw `AssetManager` if no assets.py:
```python
from assetkit import AssetManager
assets = AssetManager(package_root="my_assets", resource_dir="resources/assets")
print(assets.list())
```

---

## 👷 Development Workflow

A small `Makefile` is included to simplify common tasks:

```bash
make install  # install the package in editable mode
make test     # run the test suite
make package  # build a distribution under `dist/`
```

## 🐳 Dockerized Example (Optional)

```dockerfile
FROM python:3.12-slim

RUN pip install assetkit

WORKDIR /app
RUN assetkit new my_assets --add /dev/null --gen-assets-py

WORKDIR /app/my_assets
RUN pip install .

CMD ["python", "-c", "from my_assets.assets import assets; print(assets.myfile_txt.text())"]
```

---

## 📄 License

MIT — See [LICENSE](LICENSE)

---

## 📬 More Info

- [GitHub Repository](https://github.com/docdann/assetkit)
- [PyPI Project Page](https://pypi.org/project/assetkit/)

---

## 🏁 Roadmap (Coming Soon)

- `assetkit bundle` and `assetkit extract` CLI tooling  
- Language-agnostic `assetkit.yaml` asset manifests  
- `assetkit.ext.yaml`, `assetkit.ext.pandas` helpers  
- CLI dispatch of packaged binary tools (`assetkit run <tool>`)  
- GitHub Actions publishing workflows  
- Plugin-style extension system for asset loaders
