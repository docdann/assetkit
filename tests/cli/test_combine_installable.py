import sys
import subprocess
import tempfile
from pathlib import Path


def test_combined_asset_package_is_installable():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        pkg1 = "pkg1_assets"
        pkg2 = "pkg2_assets"
        combined = "combined_assets"

        # Step 1: Create and install two asset packages
        for name in [pkg1, pkg2]:
            result = subprocess.run(
                ["assetkit", "new", name, "--gen-assets-py", "--target-dir", str(tmp_path)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"Failed to create package {name}:\n{result.stderr}"

            install_result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "."],
                cwd=tmp_path / name,
                capture_output=True,
                text=True,
            )
            assert install_result.returncode == 0, f"pip install failed for {name}:\n{install_result.stderr}"

        # Step 2: Combine the two packages by their full paths
        build_dir = tmp_path / "_build"
        build_dir.mkdir()

        result = subprocess.run(
            [
                "assetkit", "combine",
                str(tmp_path / pkg1), str(tmp_path / pkg2),
                "--output", combined,
                "--gen-assets-py",
                "--target-dir", str(tmp_path),
            ],
            cwd=build_dir,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Combine failed:\n{result.stdout}\n{result.stderr}"

        # Step 3: Ensure combined package is pip-installable
        combined_path = tmp_path / combined
        install_combined = subprocess.run(
            [sys.executable, "-m", "pip", "install", "."],
            cwd=combined_path,
            capture_output=True,
            text=True,
        )
        assert install_combined.returncode == 0, f"pip install failed for combined package:\n{install_combined.stderr}"

        # Step 4: Verify packaging files exist
        for fname in ["setup.cfg", "pyproject.toml", "MANIFEST.in"]:
            assert (combined_path / fname).exists(), f"{fname} not found in combined package"
