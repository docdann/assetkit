# assetkit/internal/cli/bundle_docker_image.py

import subprocess
import shutil
import os
import sys
from pathlib import Path
from types import SimpleNamespace
import tempfile

from assetkit.cli.new import create_new_project
from assetkit.internal.generators.generate_asset_map import generate_asset_mapping


def bundle_docker_image_cli(args):
    image_name = args.image
    package_name = args.package
    install = args.install
    gen_assets_py = args.gen_assets_py

    # Use tmp dir by default unless --target-dir is explicitly passed
    if getattr(args, "target_dir", None):
        target_dir = Path(args.target_dir).resolve()
        temp_dir = None
    else:
        temp_dir = tempfile.TemporaryDirectory()
        target_dir = Path(temp_dir.name).resolve()

    print(f"[AssetKit] 🚀 Bundling Docker image '{image_name}' into asset package '{package_name}'")

    # Step 1: Pull image (if not already present)
    try:
        print(f"[AssetKit] Pulling Docker image: {image_name}")
        subprocess.run(["docker", "pull", image_name], check=True)
    except FileNotFoundError:
        print("[AssetKit ERROR] Docker is not installed or not in PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print(f"[AssetKit ERROR] Failed to pull image: {image_name}")
        sys.exit(1)

    # Step 2: Create base package using create_new_project()
    asset_temp_dir = target_dir / package_name
    if asset_temp_dir.exists():
        print(f"[AssetKit ERROR] Target directory already exists: {asset_temp_dir}")
        sys.exit(1)

    new_args = SimpleNamespace(
        name=package_name,
        add=[],
        install=False,
        gen_assets_py=False,
        target_dir=str(target_dir)
    )
    create_new_project(new_args)

    # Step 3: Save Docker image as image.tar
    image_tar_path = asset_temp_dir / package_name / "resources" / "assets" / "image.tar"
    image_tar_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        print(f"[AssetKit] Saving Docker image to: {image_tar_path}")
        subprocess.run(["docker", "save", "-o", str(image_tar_path), image_name], check=True)
    except subprocess.CalledProcessError:
        print(f"[AssetKit ERROR] Failed to save Docker image: {image_name}")
        sys.exit(1)

    # Step 4: Generate assets.py if requested
    if gen_assets_py:
        assets_py_path = asset_temp_dir / package_name / "assets.py"
        try:
            print(f"[AssetKit] Generating asset mapping file: {assets_py_path}")
            generate_asset_mapping(
                package_path=asset_temp_dir / package_name,
                resource_dir="resources/assets",
                output_filename=str(assets_py_path)
            )
            print(f"[AssetKit] ✅ assets.py generated successfully")
        except Exception as e:
            print(f"[AssetKit ERROR] Failed to generate assets.py: {e}")

    # Step 5: Optionally install the generated package
    if install:
        install_dir = asset_temp_dir
        print(f"[AssetKit DEBUG] Installing package from {install_dir}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "."],
            cwd=install_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"[AssetKit ERROR] Failed to install package:\n{result.stderr}")
        else:
            print(f"[AssetKit] ✅ Package installed successfully from {install_dir}")

    # Clean up temp directory if used
    if temp_dir:
        print(f"[AssetKit DEBUG] Cleaning up temporary directory: {temp_dir.name}")
        temp_dir.cleanup()


def register_bundle_docker_image_command(subparsers):
    parser = subparsers.add_parser("bundle-docker-image", help="Bundle a Docker image into an AssetKit asset package")
    parser.add_argument("image", help="Docker image name (e.g., ubuntu:22.04)")
    parser.add_argument("package", help="Asset package name to generate")
    parser.add_argument("--install", action="store_true", help="Install package after generation")
    parser.add_argument("--gen-assets-py", action="store_true", help="Generate asset mapping file (assets.py)")
    parser.add_argument("--target-dir", help="Target directory for asset package output (default: uses tmp directory)")
    parser.set_defaults(func=bundle_docker_image_cli)
