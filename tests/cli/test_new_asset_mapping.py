import subprocess
import tempfile
from pathlib import Path

def test_assetkit_new_project_asset_mapping_links_correctly():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        project_name = "test_assets_pkg"
        asset_dir = tmp_path / "extra_assets"
        asset_dir.mkdir()
        asset_file = asset_dir / "sample.txt"
        asset_file.write_text("Hello from CLI test asset")

        result = subprocess.run(
            ["assetkit", "new", project_name, "--add", str(asset_file), "--gen-assets-py", "--install"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"

        # ✅ Now this will work
        assets_py = tmp_path / project_name / project_name / "assets.py"
        assert assets_py.exists(), f"Missing generated assets.py: {assets_py}"

        # Optionally verify contents
        content = assets_py.read_text()
        assert "class AssetsProxy" in content
        assert "sample_txt" in content  # since sample.txt becomes sample_txt
