# assetkit/cli/new.py

import shutil
import subprocess
from pathlib import Path
import sys

from assetkit.internal.generators.generate_asset_map import generate_asset_mapping  # ✅ NEW

TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "asset_package"


def register_new_command(subparsers):
    parser = subparsers.add_parser("new", help="Create a new AssetKit asset package project")
    parser.add_argument("name", type=str, help="Name of the new asset package project")
    parser.add_argument(
        "--add",
        nargs="*",
        default=[],
        help="Optional list of file or directory paths to include in resources/assets/"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install the package after creation using 'pip install .'"
    )
    parser.add_argument(
        "--gen-assets-py",
        action="store_true",
        help="Generate a reusable Python asset mapping file (assets.py)"
    )
    parser.set_defaults(func=create_new_project)


def create_new_project(args):
    project_name = args.name
    asset_files = args.add
    install_flag = args.install
    gen_assets_py_flag = getattr(args, "gen_assets_py", False)

    target_path = Path.cwd() / project_name

    if target_path.exists():
        print(f"[AssetKit] Directory '{project_name}' already exists.")
        return

    print(f"[AssetKit DEBUG] Copying from template: {TEMPLATE_DIR}")
    print(f"[AssetKit DEBUG] Target path: {target_path}")

    # Copy full template to target directory
    shutil.copytree(TEMPLATE_DIR, target_path)

    # Show copied structure
    print("[AssetKit DEBUG] Files copied to target path:")
    for path in target_path.rglob("*"):
        print("  -", path.relative_to(target_path))

    # Rename 'your_package_name' dir inside new project if it exists
    old_package_dir = target_path / "your_package_name"
    new_package_dir = target_path / project_name
    if old_package_dir.exists():
        print(f"[AssetKit DEBUG] Renaming {old_package_dir} -> {new_package_dir}")
        old_package_dir.rename(new_package_dir)

    # Replace placeholders like {{PROJECT_NAME}} in all files
    print("[AssetKit DEBUG] Replacing {{PROJECT_NAME}} placeholders...")
    for path in target_path.rglob("*"):
        if path.is_file():
            try:
                content = path.read_text()
                content = content.replace("{{PROJECT_NAME}}", project_name)
                path.write_text(content)
            except UnicodeDecodeError:
                print(f"[AssetKit DEBUG] Skipped binary file: {path}")
                continue

    # Copy additional assets BEFORE generating assets.py
    asset_target_dir = new_package_dir / "resources" / "assets"
    asset_target_dir.mkdir(parents=True, exist_ok=True)

    copied_assets = []

    if asset_files:
        for path in asset_files:
            src_path = Path(path).resolve()
            if not src_path.exists():
                print(f"[AssetKit WARNING] Asset path not found: {src_path}")
                continue

            if src_path.is_file():
                dest_path = asset_target_dir / src_path.name
                shutil.copy2(src_path, dest_path)
                copied_assets.append(dest_path)
                print(f"[AssetKit DEBUG] Added file asset: {src_path} -> {dest_path}")
            elif src_path.is_dir():
                dest_dir = asset_target_dir / src_path.name
                shutil.copytree(src_path, dest_dir, dirs_exist_ok=True)
                copied_assets.append(dest_dir)
                print(f"[AssetKit DEBUG] Added directory asset: {src_path} -> {dest_dir}")

    # ✅ Generate assets.py after assets are copied
    if gen_assets_py_flag:
        output_path = (new_package_dir / "assets.py").resolve()  # ✅ ensure absolute resolved path
        print(f"[AssetKit DEBUG] Generating Python asset mapping file at {output_path}")
        try:
            generate_asset_mapping(
                package_name=project_name,
                resource_dir="resources/assets",
                output_filename=str(output_path)  # ✅ ensure correct string path
            )
            print(f"[AssetKit] Generated assets.py successfully.")
        except Exception as e:
            print(f"[AssetKit ERROR] Failed to generate asset mapping file: {e}")

    print(f"[AssetKit] Asset package project '{project_name}' created successfully at ./{project_name}/")

    # Install the package
    if install_flag:
        print(f"[AssetKit DEBUG] Installing package using 'pip install .' ...")
        subprocess.run([sys.executable, "-m", "pip", "install", "."], cwd=target_path)
