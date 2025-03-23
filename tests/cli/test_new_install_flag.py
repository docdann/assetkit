import subprocess
import sys
import tempfile
from pathlib import Path


def test_assetkit_new_project_with_install():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        project_name = "test_assets"

        result = subprocess.run(
            ["assetkit", "new", project_name, "--install"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"CLI failed: {result.stderr}"

        # Check that expected files exist in the created project
        target_path = tmp_path / project_name
        assert target_path.exists()
        assert (target_path / "setup.cfg").exists()
        assert (target_path / "pyproject.toml").exists()
        assert (target_path / "MANIFEST.in").exists()

        # ✅ Functional check: make sure installed package is importable
        check_import = subprocess.run(
            [sys.executable, "-c", f"import {project_name}"],
            capture_output=True,
            text=True
        )

        assert check_import.returncode == 0, f"Installed package {project_name} could not be imported: {check_import.stderr}"
