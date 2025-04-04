import sys
import subprocess
import tempfile
from pathlib import Path

def test_assetkit_combine_non_python_packages():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        pkg1 = "cli_assets"
        combined = "combined_cli_assets"

        # Step 1: Create a minimal non-Python assetkit-compatible package
        pkg1_path = tmp_path / pkg1
        pkg1_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists before writing

        # Root-level project files
        (pkg1_path / "pyproject.toml").write_text("[build-system]\nrequires = []\nbuild-backend = \"setuptools.build_meta\"\n")
        (pkg1_path / "MANIFEST.in").write_text("recursive-include * *\n")
        (pkg1_path / "assetkit.yaml").write_text("name: cli_assets\n")
        (pkg1_path / "setup.cfg").write_text("[metadata]\nname = cli_assets\nversion = 0.1.0\n")

        # Source dir nested inside root with same name as project
        pkg1_src = pkg1_path / pkg1
        pkg1_src.mkdir(parents=True)
        (pkg1_src / "__init__.py").write_text("# dummy module\n")
        assets_dir = pkg1_src / "resources" / "assets"
        assets_dir.mkdir(parents=True)
        (assets_dir / "hello.txt").write_text("This is a non-Python asset.\n")

        # Step 2: Combine
        build_dir = tmp_path / "_build"
        build_dir.mkdir()
        result = subprocess.run(
            [
                "assetkit", "combine", str(pkg1_path),
                "--output", combined,
                "--target-dir", str(tmp_path)
            ],
            cwd=build_dir,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Combine failed:\n{result.stdout}\n{result.stderr}"

        # Step 3: Validate structure
        combined_path = tmp_path / combined
        vendors_dir = combined_path / "resources" / "assets" / "vendors"
        assert (vendors_dir / pkg1).is_dir(), "Vendor folder missing"
        assert (vendors_dir / pkg1 / pkg1 / pkg1 / "resources" / "assets" / "hello.txt").exists(), "hello.txt missing"

        # Step 4: Ensure setup.cfg wasn't injected with pip dependency
        setup_cfg = (combined_path / "setup.cfg").read_text()
        assert "cli_assets @ file://" not in setup_cfg
