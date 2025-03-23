import os
from pathlib import Path
from typing import Dict, List, Union
from importlib.resources import files as pkg_files


class AssetFile:
    def __init__(self, path_obj: Path):
        self._path = path_obj

    def text(self) -> str:
        return self._path.read_text(encoding="utf-8")

    def bytes(self) -> bytes:
        return self._path.read_bytes()

    def path(self) -> str:
        return str(self._path.resolve())

    def __repr__(self):
        return f"<AssetFile path='{self.path()}' size={len(self.bytes())} bytes>"


class AssetManager:
    def __init__(self, package_root: Union[str, Path], resource_dir: str = "resources/assets"):
        """
        Initialize asset manager.

        :param package_root: A package name (str) OR filesystem path (Path or str)
        :param resource_dir: Relative resource path (default: "resources/assets")
        """
        if isinstance(package_root, (str, Path)) and Path(package_root).exists():
            # Filesystem path mode
            self._base = Path(package_root).resolve() / resource_dir
            if not self._base.exists():
                raise FileNotFoundError(f"AssetManager: Resource directory not found at path: {self._base}")
        else:
            # Installed package mode
            try:
                self._base = pkg_files(package_root) / resource_dir
            except ModuleNotFoundError:
                raise RuntimeError(f"AssetManager: Package '{package_root}' is not installed or discoverable")
            if not self._base.exists():
                raise FileNotFoundError(f"AssetManager: Resource directory not found in package: {self._base}")

        self._index = self._build_index()

    def _build_index(self) -> Dict[str, AssetFile]:
        index = {}

        def walk(path_obj, prefix=""):
            for item in path_obj.iterdir():
                rel = os.path.join(prefix, item.name).replace("\\", "/")
                if item.is_dir():
                    walk(item, rel)
                else:
                    index[rel] = AssetFile(item)

        walk(self._base)
        return index

    def __getitem__(self, key: str) -> AssetFile:
        if key not in self._index:
            raise KeyError(f"Asset not found: {key}")
        return self._index[key]

    def list(self) -> List[str]:
        return list(self._index.keys())

    def find(self, suffix: str) -> List[str]:
        return [k for k in self._index if k.endswith(suffix)]

    def __contains__(self, key: str) -> bool:
        return key in self._index

    def __repr__(self):
        return f"<AssetManager {len(self._index)} assets>"
