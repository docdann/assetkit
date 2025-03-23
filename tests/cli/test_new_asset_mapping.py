import subprocess
import tempfile
import importlib.util
from pathlib import Path


def import_generated_assets_module(package_path: Path, project_name: str):
    """
    Dynamically import the generated assets.py file from the installed asset package path.
    """
    # ✅ Correct location of the generated file
    assets_py_path = package_path / project_name / project_name / "assets.py"
    assert assets_py_path.exists(), f"Missing generated assets.py: {assets_py_path}"

    spec = importlib.util.spec_from_file_location(f"{project_name}.assets", str(assets_py_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_assetkit_new_project_asset_mapping_links_correctly():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        project_name = "test_assets_pkg"

        # Create a dummy asset file
        asset_dir = tmp_path / "extra_assets"
        asset_dir.mkdir()
        asset_file = asset_dir / "sample.txt"
        asset_file.write_text("Hello from CLI test asset")

        # Run `assetkit new` with install and mapping generation
        result = subprocess.run(
            ["assetkit", "new", project_name, "--add", str(asset_file), "--install", "--gen-assets-py"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"CLI failed: {result.stderr}"

        # Dynamically import the generated assets module
        module = import_generated_assets_module(tmp_path, project_name)

        # Check the attribute exists in the mapping
        assert hasattr(module.assets, "sample_txt"), "Expected 'sample_txt' attribute not found in assets proxy"

        # Check asset content
        content = module.assets.sample_txt.text()
        assert "Hello from CLI test asset" in content
