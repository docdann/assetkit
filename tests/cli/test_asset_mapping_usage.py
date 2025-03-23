import importlib.util
import tempfile
import subprocess
from pathlib import Path


def import_generated_assets_module(package_path: Path, project_name: str):
    """
    Dynamically import the generated assets.py file from the installed asset package path.
    Returns the imported module object.
    """
    assets_py = package_path / project_name / project_name / "assets.py"
    assert assets_py.exists(), f"Missing generated assets.py: {assets_py}"

    spec = importlib.util.spec_from_file_location(f"{project_name}.assets", str(assets_py))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_assetkit_asset_mapping_usage_smoke():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        project_name = "test_assets_usage"
        extra_assets_dir = tmp_path / "assets"
        extra_assets_dir.mkdir()
        dummy_asset = extra_assets_dir / "dummy.txt"
        dummy_asset.write_text("Hello from test_asset_mapping_usage")

        # Create asset package via AssetKit CLI
        result = subprocess.run(
            ["assetkit", "new", project_name, "--add", str(dummy_asset), "--gen-assets-py", "--install"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"AssetKit CLI failed:\n{result.stdout}\n{result.stderr}"

        # Import the generated assets.py file
        module = import_generated_assets_module(tmp_path, project_name)
        assets = module.assets

        # Assert at least one expected attribute exists
        found_assets = [
            attr for attr in dir(assets)
            if not attr.startswith("_") and hasattr(getattr(assets, attr), "path")
        ]
        assert found_assets, "No asset attributes found in assets proxy"

        # Try reading contents of each mapped asset
        for attr in found_assets:
            asset = getattr(assets, attr)
            path = asset.path()
            print(f"[TEST] {attr}: {path}")
            assert Path(path).exists(), f"Asset file {path} does not exist"

            # Try reading the text content
            try:
                content = asset.text()
                assert "Hello" in content or content.strip() != "", f"Asset {attr} content appears empty"
            except UnicodeDecodeError:
                # Acceptable for binary files
                content_bytes = asset.bytes()
                assert len(content_bytes) > 0, f"Asset {attr} content appears empty (binary)"
