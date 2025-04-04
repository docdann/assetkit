# AssetKit Combine Command

This module provides the `assetkit combine` CLI command, allowing you to **merge multiple AssetKit packages** into a single reusable and optionally installable meta-package.

## 🚀 Features

- ✅ Combine multiple asset packages into a single structured package.
- 📦 Automatically extracts `.tar.gz` exports of each sub-package.
- 🧩 Maintains a recursive vendor tree under `resources/assets/vendors/`.
- 🔁 Supports combining both Python-based and non-Python asset packages.
- 🧠 Optionally generates an `assets.py` map for easy asset access.
- 📥 Optionally installs the combined package via `pip`.

## 🧪 Example

```bash
# Combine two existing packages into a new one
assetkit combine my_assets1 my_assets2 --output combined_assets --gen-assets-py --install
```

## 📁 Directory Structure

```
combined_assets/
├── combined_assets/
│   ├── __init__.py
│   ├── assets.py         # Optional
│   └── resources/
│       └── assets/
│           └── vendors/
│               ├── pkg1_assets/
│               └── pkg2_assets/
├── setup.cfg
├── pyproject.toml
└── MANIFEST.in
```

## 🔄 Reusability

The resulting combined package:

- Is pip-installable
- Retains the full AssetKit package structure
- Can itself be passed back into `assetkit combine` for infinite composability

## ⚠️ Notes

- Only packages with `setup.cfg` or `pyproject.toml` will be added to `install_requires`.
- Non-Python packages are skipped from pip dependencies but still included as extracted resources.

## 🔧 CLI Reference

```bash
assetkit combine <package1> <package2> ... \
  --output <name> \
  [--target-dir <path>] \
  [--gen-assets-py] \
  [--install]
```

## 🧬 Dependencies

This module assumes:
- Python 3.7+
- AssetKit installed (`pip install assetkit`)
- Valid asset packages created via `assetkit new`

## 📚 License

MIT or project license.
