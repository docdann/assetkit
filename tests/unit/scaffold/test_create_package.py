import tempfile
import shutil
from pathlib import Path
from assetkit.scaffold import create_package

def safe_rmtree(path, max_retries=5, delay=0.5):
    import time
    for i in range(max_retries):
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            if i == max_retries - 1:
                raise
            time.sleep(delay)

def test_create_package_generates_expected_structure():
    tmpdir = tempfile.mkdtemp()
    try:
        tmp_path = Path(tmpdir)
        package_name = "test_assets_package"
        create_package(package_name, path=tmp_path)

        pkg_root = tmp_path / package_name
        pkg_dir = pkg_root / package_name
        assert pkg_root.exists()
        assert pkg_dir.exists()
        assert (pkg_root / "pyproject.toml").exists()
        assert (pkg_root / "README.md").exists()
        assert (pkg_root / "main.py").exists()
        assert (pkg_dir / "__init__.py").exists()
        assert (pkg_dir / "resources").exists()
    finally:
        safe_rmtree(tmpdir)

def test_create_package_replaces_template_content():
    tmpdir = tempfile.mkdtemp()
    try:
        tmp_path = Path(tmpdir)
        package_name = "test_assets_package"
        create_package(package_name, path=tmp_path)

        pyproject_content = (tmp_path / package_name / "pyproject.toml").read_text()
        readme_content = (tmp_path / package_name / "README.md").read_text()
        main_content = (tmp_path / package_name / "main.py").read_text()

        assert f'name = "{package_name}"' in pyproject_content
        assert f"# {package_name}" in readme_content
        assert f'AssetManager(package_root="{package_name}"' in main_content
    finally:
        safe_rmtree(tmpdir)
