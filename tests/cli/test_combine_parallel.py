import sys
import subprocess
import tempfile
from pathlib import Path

def test_assetkit_combine_parallel_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        pkg1 = "pkg1_assets"
        pkg2 = "pkg2_assets"
        combined = "combined_assets"

        # Step 1: Create and install two asset packages using `assetkit new`
        pkg_paths = []
        for name in [pkg1, pkg2]:
            result = subprocess.run(
                ["assetkit", "new", name, "--gen-assets-py", "--target-dir", str(tmp_path)],
                cwd=tmp_path,
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"Failed to create package {name}:\n{result.stdout}\n{result.stderr}"

            pkg_install_path = tmp_path / name
            pkg_paths.append(str(pkg_install_path))

            install_result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "."],
                cwd=pkg_install_path,
                capture_output=True,
                text=True,
            )
            assert install_result.returncode == 0, f"Pip install failed for {name}:\n{install_result.stdout}\n{install_result.stderr}"

        # Step 2: Combine using full paths to the packages
        build_dir = tmp_path / "_build"
        build_dir.mkdir()

        result = subprocess.run(
            [
                "assetkit", "combine", *pkg_paths,
                "--output", combined,
                "--gen-assets-py",
                "--target-dir", str(tmp_path),
            ],
            cwd=build_dir,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Combine failed:\n{result.stdout}\n{result.stderr}"

        # Step 3: Validate structure of the combined package
        combined_pkg_dir = tmp_path / combined
        assert (combined_pkg_dir / "__init__.py").exists(), "__init__.py not found in combined package"
        assert (combined_pkg_dir / "assets.py").exists(), "assets.py not found in combined package"

        vendors_dir = combined_pkg_dir / "resources" / "assets" / "vendors"
        assert (vendors_dir / pkg1).is_dir(), f"Extracted folder for {pkg1} not found under vendors/"
        assert (vendors_dir / pkg2).is_dir(), f"Extracted folder for {pkg2} not found under vendors/"
