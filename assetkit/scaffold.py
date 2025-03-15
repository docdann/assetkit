import os
from pathlib import Path

TEMPLATE = {
    "pyproject.toml": """[project]
name = "{name}"
version = "0.1.0"

[tool.setuptools.package-data]
{name} = ["resources/**/*"]

[project.entry-points."assetkit.assets"]
{name} = "{name}"
""",
    "__init__.py": "# {name} package"
}

def create_package(name: str, path="."):
    pkg_root = Path(path) / name
    pkg_dir = pkg_root / name
    resources = pkg_dir / "resources"

    pkg_root.mkdir(parents=True, exist_ok=True)
    pkg_dir.mkdir(parents=True, exist_ok=True)
    resources.mkdir(parents=True, exist_ok=True)

    (pkg_root / "pyproject.toml").write_text(TEMPLATE["pyproject.toml"].format(name=name))
    (pkg_dir / "__init__.py").write_text(TEMPLATE["__init__.py"].format(name=name))
