# assetkit/cli/scaffold.py

import argparse
import os
import shutil
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "scaffolds"

def scaffold_project(app_type: str, name: str):
    scaffold_dir = TEMPLATES_DIR / app_type
    if not scaffold_dir.exists():
        print(f"[AssetKit] Error: Unknown scaffold type '{app_type}'")
        return

    target_dir = Path.cwd() / name
    if target_dir.exists():
        print(f"[AssetKit] Error: Directory '{name}' already exists.")
        return

    shutil.copytree(scaffold_dir, target_dir)

    # Rename placeholders in copied files
    for path in target_dir.rglob("*"):
        if path.is_file():
            content = path.read_text()
            content = content.replace("{{PROJECT_NAME}}", name)
            path.write_text(content)

    print(f"[AssetKit] Project scaffold '{name}' created successfully at ./{name}/")

def register_scaffold_command(subparsers):
    parser = subparsers.add_parser("scaffold", help="Create a consumer application scaffold")
    parser.add_argument("app_type", type=str, help="Type of scaffold to generate (e.g., mlkit)")
    parser.add_argument("name", type=str, help="Name of the new project directory")
    parser.set_defaults(func=lambda args: scaffold_project(args.app_type, args.name))
