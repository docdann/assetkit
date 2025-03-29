import tarfile
import tempfile
import subprocess
import sys
from pathlib import Path


def test_exported_tarball_is_pip_installable():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        package_name = "test_export_install"

        # Step 1: Create and export the package
        result = subprocess.run(
            ["assetkit", "new", package_name, "--gen-assets-py"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"AssetKit new failed:\n{result.stderr}"

        export_result = subprocess.run(
            ["assetkit", "export", package_name],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        assert export_result.returncode == 0, f"Export failed:\n{export_result.stderr}"

        # Step 2: Extract the tarball
        tarball_path = tmp_path / f"{package_name}.tar.gz"
        assert tarball_path.exists(), "Exported tar.gz file not found"

        install_dir = tmp_path / "unpacked"
        install_dir.mkdir()

        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(path=install_dir, filter="data")  # ✅ Python 3.14+ compatible

        # Step 3: Install extracted package
        extracted_pkg = next(install_dir.glob(f"{package_name}*"))
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "."],
            cwd=extracted_pkg,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Pip install failed:\n{result.stderr}"
