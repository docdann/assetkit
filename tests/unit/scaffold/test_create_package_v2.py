import unittest
import tempfile
import shutil
from pathlib import Path
from assetkit.scaffold import create_package

class TestScaffold(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_create_package(self):
        package_name = "test_package"
        create_package(name=package_name, path=self.temp_dir)

        pkg_root = Path(self.temp_dir) / package_name
        pkg_dir = pkg_root / package_name
        resources = pkg_dir / "resources"

        # Check directories
        self.assertTrue(pkg_root.exists())
        self.assertTrue(pkg_dir.exists())
        self.assertTrue(resources.exists())

        # Check files
        self.assertTrue((pkg_root / "pyproject.toml").exists())
        self.assertTrue((pkg_root / "README.md").exists())
        self.assertTrue((pkg_dir / "__init__.py").exists())
        self.assertTrue((pkg_root / "main.py").exists())

        # Check file content
        pyproject_content = (pkg_root / "pyproject.toml").read_text()
        self.assertIn(f'name = "{package_name}"', pyproject_content)

if __name__ == "__main__":
    unittest.main()