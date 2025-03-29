import tarfile
from pathlib import Path
import sys
import os

EXCLUDE_NAMES = {"__pycache__", "build", "dist"}
EXCLUDE_EXTENSIONS = {".pyc", ".pyo"}
EXCLUDE_DIR_SUFFIXES = {".egg-info"}

def should_exclude_path(path: Path) -> bool:
    # Skip if any part of the path matches known directory names or suffixes
    for part in path.parts:
        if part in EXCLUDE_NAMES:
            return True
        if any(part.endswith(suffix) for suffix in EXCLUDE_DIR_SUFFIXES):
            return True
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    return False

def export_package_cli(args):
    package_name = args.package
    archive_path = Path.cwd() / f"{package_name}.tar.gz"
    package_dir = Path.cwd() / package_name

    print(f"[AssetKit] Exporting package '{package_name}' to archive: {archive_path}")

    if not package_dir.exists():
        print(f"[AssetKit ERROR] Package directory does not exist: {package_dir}")
        sys.exit(1)

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            for root, dirs, files in os.walk(package_dir):
                root_path = Path(root)
                # Prune disallowed directories in-place
                dirs[:] = [
                    d for d in dirs
                    if not should_exclude_path(root_path / d)
                ]
                for file in files:
                    full_path = root_path / file
                    rel_path = full_path.relative_to(package_dir.parent)
                    if not should_exclude_path(rel_path):
                        tar.add(full_path, arcname=rel_path)
        print(f"[AssetKit] Archive created: {archive_path}")
    except Exception as e:
        print(f"[AssetKit ERROR] Failed to export package: {e}")
        sys.exit(1)

def register_export_package_command(subparsers):
    parser = subparsers.add_parser(
        "export", help="Export an asset package to a .tar.gz archive"
    )
    parser.add_argument("package", help="Name of the asset package directory to archive")
    parser.set_defaults(func=export_package_cli)
