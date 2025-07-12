import os
import tarfile
import shutil
import tempfile
from pathlib import Path


def get_registry_path() -> Path:
    """Return the path to the local registry. Creates it if needed."""
    registry = Path(os.environ.get("ASSETKIT_REGISTRY", "~/.assetkit/registry")).expanduser()
    registry.mkdir(parents=True, exist_ok=True)
    return registry


def _create_tarball(source: Path, dest: Path) -> None:
    """Create a gzipped tarball from a directory."""
    with tarfile.open(dest, "w:gz") as tar:
        tar.add(source, arcname=source.name)


def push_package(path: Path) -> Path:
    """Push a package directory or archive to the registry.

    Returns the path to the stored archive in the registry.
    """
    registry = get_registry_path()
    if path.is_dir():
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / f"{path.name}.tar.gz"
            _create_tarball(path, archive)
            dest = registry / archive.name
            shutil.copy2(archive, dest)
    else:
        dest = registry / path.name
        shutil.copy2(path, dest)
    print(f"[AssetKit] Registry push: {dest}")
    return dest


def pull_package(name: str, output_dir: Path) -> Path:
    """Pull a package from the registry and extract it.

    Returns the path to the extracted directory.
    """
    registry = get_registry_path()
    filename = name if name.endswith(".tar.gz") else f"{name}.tar.gz"
    archive = registry / filename
    if not archive.exists():
        raise FileNotFoundError(f"Package not found in registry: {name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(path=output_dir)
    print(f"[AssetKit] Registry pull: extracted {archive} -> {output_dir}")
    return output_dir / archive.stem


def list_packages() -> list:
    """List package archives stored in the registry (base names)."""
    registry = get_registry_path()
    return sorted(p.stem for p in registry.glob("*.tar.gz"))
