# 📦 AssetKit + GitHub Repo Packaging Demo

This example demonstrates how to use **AssetKit** to create a pip-installable Python asset package that includes the contents of a **cloned GitHub repository** inside its `resources/assets/` directory.

The entire process is containerized using **Docker**, ensuring a reproducible and portable build.

---

## 🚀 What This Demo Shows

- How to scaffold a new asset package using `assetkit new my_assets`
- How to clone a GitHub repository into `resources/assets/github_repo/`
- How to install the package using `pip install .`
- How to access the GitHub repo contents at runtime using `AssetManager`

---

## 🔧 Project Structure After Build

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
            └── github_repo/
                ├── README
                └── ... other GitHub repo files ...
```

---

## 🐳 Dockerfile Overview

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir assetkit

WORKDIR /app

RUN assetkit new my_assets

# Ensure correct nested path in installable package
RUN mkdir -p /app/my_assets/my_assets/resources/assets \
    && git clone https://github.com/octocat/Hello-World.git /app/my_assets/my_assets/resources/assets/github_repo

RUN ls -R /app/my_assets/my_assets/resources/assets

WORKDIR /app/my_assets
RUN pip install --no-cache-dir .

CMD ["python", "-c", "from assetkit import AssetManager; \
assets = AssetManager(package_root='my_assets', resource_dir='resources/assets'); \
print('Assets at runtime:', assets.list())"]
```

---

## 🛠 How to Build and Run

```bash
docker build -t assetkit-demo --no-cache .
docker run --rm assetkit-demo
```

### ✅ Expected Output
```
Assets at runtime: ['config/model.yaml', 'data/sample.csv', 'github_repo/README', ...]
```

---

## 📌 Key Takeaways

- **AssetKit** lets you create modular asset packages with structured file trees.
- Assets (even from external sources like GitHub) can be injected into the package pre-install and accessed cleanly at runtime.
- Using `pip install .` and proper `setup.cfg` + `MANIFEST.in` configuration ensures all files are included.

---

## 🔗 Related Links
- AssetKit: https://pypi.org/project/assetkit/
- GitHub Example Repo: https://github.com/octocat/Hello-World

