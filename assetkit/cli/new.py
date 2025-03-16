# assetkit/cli/new.py

import shutil
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "asset_package"

def register_new_command(subparsers):
    parser = subparsers.add_parser("new", help="Create a new AssetKit asset package project")
    parser.add_argument("name", type=str, help="Name of new asset package")
    parser.set_defaults(func=create_new_project)

def create_new_project(args):
    project_name = args.name
    target_path = Path.cwd() / project_name

    if target_path.exists():
        print(f"[AssetKit] Directory '{project_name}' already exists.")
        return

    shutil.copytree(TEMPLATE_DIR, target_path)
    print(f"[AssetKit] Asset package project '{project_name}' created at ./{project_name}/")
