# assetkit/internal/cli/load_docker_image.py

import subprocess
import sys
from pathlib import Path

from assetkit.asset_manager import AssetManager


def load_docker_image_cli(args):
    package = args.package
    asset_key = args.asset

    print(f"[AssetKit] 🔍 Loading Docker image from installed package '{package}' (asset key: '{asset_key}')")

    # Attempt loading from installed package first
    try:
        assets = AssetManager(package_root=package, resource_dir="resources/assets")
    except Exception as e:
        print(f"[AssetKit WARNING] Could not load as installed package: {e}")
        print(f"[AssetKit] ➡ Falling back to local path: ./{package}/resources/assets")
        try:
            fallback_path = Path.cwd() / package
            assets = AssetManager(package_root=fallback_path, resource_dir="resources/assets")
        except Exception as inner_e:
            print(f"[AssetKit ERROR] Failed to load AssetManager from fallback path: {inner_e}")
            sys.exit(1)

    if asset_key not in assets:
        print(f"[AssetKit ERROR] Asset key '{asset_key}' not found in package '{package}'")
        print("Available assets:")
        for k in assets.list():
            print(f"  - {k}")
        sys.exit(1)

    tar_path = assets[asset_key].path()
    try:
        subprocess.run(["docker", "load", "-i", tar_path], check=True)
        print(f"[AssetKit] ✅ Docker image loaded successfully from {tar_path}")
    except subprocess.CalledProcessError as e:
        print(f"[AssetKit ERROR] Failed to load Docker image from tar: {e}")
        sys.exit(1)


def register_load_docker_image_command(subparsers):
    parser = subparsers.add_parser("load-docker", help="Load a Docker image from an asset package")
    parser.add_argument("package", help="Name of the installed asset package or local package directory")
    parser.add_argument("asset", help="Asset key for the Docker image tarball (e.g., 'image.tar')")
    parser.set_defaults(func=load_docker_image_cli)
