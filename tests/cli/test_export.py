# tests/cli/test_export_clean.py

import tempfile
import subprocess
import tarfile
from pathlib import Path
import sys


def test_exported_tarball_is_clean_and_installable():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        project_name = "export_clean_test"

        # Step 1: Create package
        result = subprocess.run(
            ["assetkit", "new", project_name, "--install"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Creation failed:\n{result.stderr}\n{result.stdout}"

        # Step 2: Export package
        result = subprocess.run(
            ["assetkit", "export", project_name],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Export failed:\n{result.stderr}\n{result.stdout}"

        archive_path = tmp_path / f"{project_name}.tar.gz"
        assert archive_path.exists(), f"Expected tarball not found: {archive_path}"

        # Step 3: Check for unwanted files
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
            forbidden = [n for n in names if any(part in n for part in ["__pycache__", ".pyc", ".pyo", "build", "dist", ".egg-info"])]
            assert not forbidden, f"Tarball contains unwanted files: {forbidden}"

        # Step 4: Install from extracted archive
        install_dir = tmp_path / "install"
        install_dir.mkdir()

        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(install_dir, filter='data')

        pkg_root = install_dir / project_name
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "."],
            cwd=pkg_root,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Pip install from tarball failed:\n{result.stderr}\n{result.stdout}"
