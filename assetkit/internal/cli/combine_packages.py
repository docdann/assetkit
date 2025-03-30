import sys
import os
import subprocess
import tempfile
import tarfile
from pathlib import Path
from types import SimpleNamespace

from assetkit.asset_manager import AssetManager
from assetkit.internal.generators.generate_asset_map import generate_asset_mapping
from assetkit.cli.new import create_new_project
from assetkit.internal.cli.export_package import export_package_cli as export_project

def extract_tar_to_dir(tar_path, extract_to):
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_to)

def append_local_dependency_to_setup_cfg(setup_cfg_path, pkg_name, relative_path):
    with open(setup_cfg_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_install_requires = False
    found_options = False
    found_install_requires = False
    new_lines = []
    inserted = False

    for line in lines:
        stripped = line.strip()

        if stripped == "[options]":
            found_options = True

        if stripped.startswith("install_requires") and found_options:
            found_install_requires = True
            in_install_requires = True
            new_lines.append(line)
            continue

        if in_install_requires and (stripped == "" or stripped.startswith("[")):
            new_lines.append(f"    {pkg_name} @ file://{relative_path}\n")
            inserted = True
            in_install_requires = False

        new_lines.append(line)

    if not found_install_requires and found_options:
        index = next(i for i, line in enumerate(new_lines) if line.strip() == "[options]") + 1
        new_lines.insert(index, "install_requires =\n")
        new_lines.insert(index + 1, f"    {pkg_name} @ file://{relative_path}\n")
        inserted = True

    if not found_options:
        new_lines.append("\n[options]\n")
        new_lines.append("install_requires =\n")
        new_lines.append(f"    {pkg_name} @ file://{relative_path}\n")
        inserted = True

    if not inserted:
        raise RuntimeError("Could not insert dependency into setup.cfg")

    with open(setup_cfg_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def combine_packages_cli(args):
    package_names = args.packages
    combined_name = args.output
    base_dir = Path(args.target_dir or tempfile.gettempdir())
    target_dir = base_dir / combined_name
    print(f"[AssetKit] Combining packages into: {target_dir}")

    if target_dir.exists():
        print(f"[AssetKit ERROR] Output directory already exists: {target_dir}")
        sys.exit(1)

    print("[AssetKit] Bootstrapping base project...")
    dummy_args = SimpleNamespace(
        name=combined_name,
        target_dir=str(base_dir),
        add=[],
        install=False,
        gen_assets_py=False,
        quiet=True,
    )
    create_new_project(dummy_args)

    package_root = target_dir
    vendor_root = package_root / "resources" / "assets" / "vendors"
    vendor_root.mkdir(parents=True, exist_ok=True)

    init_lines = []
    for pkg_arg in package_names:
        try:
            pkg_path = Path(pkg_arg).resolve()
            pkg_name = pkg_path.name if pkg_path.exists() else pkg_arg

            if not pkg_path.exists():
                site_pkg = next((Path(p) for p in sys.path if (Path(p) / pkg_arg).exists()), None)
                if not site_pkg:
                    raise FileNotFoundError(f"Could not locate installed package or path: {pkg_arg}")
                pkg_path = site_pkg / pkg_arg

            print(f"[AssetKit] + Adding: {pkg_name}")
            export_path = vendor_root / f"{pkg_name}.tar.gz"

            cwd_backup = Path.cwd()
            try:
                os.chdir(str(export_path.parent))
                export_args = SimpleNamespace(
                    package=str(pkg_path),
                    quiet=True,
                    format="gztar",
                )
                export_project(export_args)
            finally:
                os.chdir(str(cwd_backup))

            if not export_path.exists():
                raise FileNotFoundError(f"Export failed: {export_path} not created")

            extract_to = vendor_root / pkg_name
            extract_to.mkdir(parents=True, exist_ok=True)
            extract_tar_to_dir(export_path, extract_to)
            export_path.unlink()

            init_lines.append(f"# vendored: {pkg_name} -> resources/assets/vendors/{pkg_name}/")

            is_python_pkg = (extract_to / "setup.cfg").exists() or (extract_to / "pyproject.toml").exists()
            if is_python_pkg:
                setup_cfg_path = package_root / "setup.cfg"
                rel_path = f"./resources/assets/vendors/{pkg_name}"
                append_local_dependency_to_setup_cfg(setup_cfg_path, pkg_name, rel_path)
            else:
                print(f"[AssetKit] Skipping pip dependency for non-Python asset package: {pkg_name}")

        except Exception as e:
            print(f"[AssetKit ERROR] Failed to export package '{pkg_arg}': {e}")
            print(f"[AssetKit ERROR] Could not determine project root from: {pkg_path}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    init_file = package_root / "__init__.py"
    with open(init_file, "a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(init_lines) + "\n")

    if args.gen_assets_py:
        output_file = package_root / "assets.py"
        assets_path = package_root / "resources" / "assets"
        if assets_path.exists():
            generate_asset_mapping(
                package_path=package_root,
                resource_dir="resources/assets",
                output_filename=output_file,
            )
            with open(init_file, "a", encoding="utf-8") as f:
                f.write("\nfrom .assets import assets\n")
        else:
            print("[AssetKit] Skipping assets.py generation — no resources/assets directory found.")

    if args.install:
        print(f"[AssetKit] Installing combined package with pip...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "."],
            cwd=target_dir,
            check=True
        )

    print(f"[AssetKit] Combined package created at: {target_dir}")

def register_combine_command(subparsers):
    parser = subparsers.add_parser(
        "combine",
        help="Combine multiple asset packages into one meta-package"
    )
    parser.add_argument("packages", nargs="+", help="Names or paths of asset packages to combine")
    parser.add_argument("--output", required=True, help="Name of the new combined package")
    parser.add_argument("--target-dir", help="Directory to write the combined package (default: temp dir)")
    parser.add_argument("--gen-assets-py", action="store_true", help="Generate assets.py mapping")
    parser.add_argument("--install", action="store_true", help="Install the combined package after creation")
    parser.set_defaults(func=combine_packages_cli)