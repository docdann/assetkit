# 📦 AssetKit + GitHub Binary Packaging Demo

This example demonstrates how to use **AssetKit** to create a pip-installable Python asset package that includes a **native binary executable from a GitHub repository** — in this case, the [`bat`](https://github.com/sharkdp/bat) CLI tool.

The entire workflow is containerized using **Docker**, making the process reproducible and portable.

---

## 🚀 What This Demo Shows

- Scaffold a new AssetKit asset package using `assetkit new`
- Download and extract a binary release (e.g., `bat`) into the `resources/assets` directory
- Install the asset package via `pip install .`
- Access and execute the binary **at runtime** using AssetKit's `AssetManager`

---

## 📁 Final Package Structure

```
/app/my_assets/
├── setup.cfg
├── pyproject.toml
├── MANIFEST.in
└── my_assets/
    ├── __init__.py
    └── resources/
        └── assets/
            ├── config/
            │   └── model.yaml
            ├── data/
            │   └── sample.csv
            └── bat_bin/
                ├── bat
                ├── LICENSE
                └── ...
```

---

## 🐳 Dockerfile Summary

The `Dockerfile` does the following:
- Installs AssetKit and system dependencies (git, curl, tar)
- Creates a new asset package via `assetkit new my_assets`
- Downloads and extracts `bat` CLI binary into the assets directory
- Installs the asset package via `pip install .`
- At runtime, uses `AssetManager` to access and execute the binary

### Full `Dockerfile`:
```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y git curl tar && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir assetkit

WORKDIR /app

RUN assetkit new my_assets

RUN mkdir -p /app/my_assets/my_assets/resources/assets/bat_bin \
    && curl -L https://github.com/sharkdp/bat/releases/download/v0.24.0/bat-v0.24.0-x86_64-unknown-linux-gnu.tar.gz -o bat.tar.gz \
    && tar -xzf bat.tar.gz -C /app/my_assets/my_assets/resources/assets/bat_bin --strip-components=1 \
    && rm bat.tar.gz

RUN ls -R /app/my_assets/my_assets/resources/assets/bat_bin

WORKDIR /app/my_assets
RUN pip install --no-cache-dir .

CMD ["python", "-c", "
from assetkit import AssetManager;
import subprocess;
assets = AssetManager(package_root='my_assets', resource_dir='resources/assets');
bat_path = assets['bat_bin/bat'].path();
print('Running bat from asset package:');
subprocess.run([bat_path, '--version'])
"]
```

---

## 🛠 How to Build & Run

### Build the Docker Image:
```bash
docker build --no-cache -t assetkit-binary-demo .
```

### Run the Container:
```bash
docker run --rm assetkit-binary-demo
```

### ✅ Expected Output:
```
Running bat from asset package:
bat 0.24.0
```

---

## 💡 Key Takeaways

- You can bundle **non-Python tools (binaries, executables)** inside an **AssetKit resource package**
- Everything is installed via `pip install .` and accessed cleanly using `AssetManager`
- Great for bundling CLI tools, ML binaries, native compiled libs, etc.

---

## 🔗 References
- [AssetKit on PyPI](https://pypi.org/project/assetkit/)
- [AssetKit GitHub](https://github.com/docdann/assetkit)
- [bat GitHub Repository](https://github.com/sharkdp/bat)
