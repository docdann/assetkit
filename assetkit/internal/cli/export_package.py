import tarfile
from pathlib import Path
import sys
import os

EXCLUDE_NAMES = {"__pycache__", "build", "dist"}
EXCLUDE_EXTENSIONS = {".pyc", ".pyo"}
EXCLUDE_DIR_SUFFIXES = {".egg-info"}

def should_exclude_path(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_NAMES:
            return True
        if any(part.endswith(suffix) for suffix in EXCLUDE_DIR_SUFFIXES):
            return True
    if path.suffix in EXCLUDE_EXTENSIONS:
        return True
    return False

def export_package_cli(args):
    package_path = Path(args.package).resolve()
    package_name = package_path.name

    # Root of the project (may be parent of the actual package directory)
    if (package_path / "setup.cfg").exists():
        # It's already the project root
        project_root = package_path
    elif (package_path.parent / "setup.cfg").exists():
        # Treat parent as the project root
        project_root = package_path.parent
    else:
        print(f"[AssetKit ERROR] Could not determine project root from: {package_path}")
        sys.exit(1)

    if hasattr(args, "output") and args.output:
        archive_path = Path(args.output).resolve()
    else:
        archive_path = Path.cwd() / f"{project_root.name}.tar.gz"

    print(f"[AssetKit] Exporting package '{project_root}' to archive: {archive_path}")

    if not project_root.exists():
        print(f"[AssetKit ERROR] Package directory does not exist: {project_root}")
        sys.exit(1)

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            for root, dirs, files in os.walk(project_root):
                root_path = Path(root)
                dirs[:] = [d for d in dirs if not should_exclude_path(root_path / d)]
                for file in files:
                    full_path = root_path / file
                    rel_path = full_path.relative_to(project_root.parent)
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
    parser.add_argument("package", help="Name or path to the asset package directory or root project directory")
    parser.add_argument("--output", help="Optional path to write the archive to")
    parser.set_defaults(func=export_package_cli)
