# 📦 assetkit bundle-docker-image

AssetKit now supports bundling Docker images as structured, pip-installable asset packages.

---

## 🚀 Overview

With `assetkit bundle-docker-image`, you can:

- Pull a Docker image (e.g., `ubuntu:22.04`)
- Save it as a `resources/assets/image.tar` inside a new AssetKit package
- Auto-generate an `assets.py` mapping file (optional)
- Make it pip-installable and reusable
- Use `assetkit load-docker` to restore the image later

---

## 🔧 CLI Usage

### Bundle a Docker image:
```bash
assetkit bundle-docker-image ubuntu:22.04 ubuntu_assets
```

### Bundle + install package:
```bash
assetkit bundle-docker-image ubuntu:22.04 ubuntu_assets --install
```

### Bundle + generate `assets.py` mapping:
```bash
assetkit bundle-docker-image ubuntu:22.04 ubuntu_assets --install --gen-assets-py
```

### Specify a custom target directory:
```bash
assetkit bundle-docker-image ubuntu:22.04 ubuntu_assets --target-dir ./bundles/
```

---

## 📂 Package Structure

```
ubuntu_assets/
├── pyproject.toml
├── setup.cfg
├── MANIFEST.in
└── ubuntu_assets/
    ├── __init__.py
    ├── assets.py            # Optional if --gen-assets-py
    └── resources/
        └── assets/
            └── image.tar    # Docker image saved here
```

---

## 🐳 Load Docker Image Later

```bash
assetkit load-docker ubuntu_assets image.tar
```

Or in Python:
```python
from ubuntu_assets.assets import assets
print(assets.image_tar.path())
```

Or use AssetManager directly:
```python
from assetkit import AssetManager
assets = AssetManager(package_root="ubuntu_assets")
print(assets["image.tar"].path())
```

---

## ✅ Benefits

- Offline Docker image loading
- Pip-installable container assets
- Secure, reproducible container workflows
- Easily distributed via `.whl`

---
