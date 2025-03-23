import tempfile
import subprocess
from pathlib import Path
import pytest


@pytest.mark.integration
def test_bundle_and_load_docker_image():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        package_name = "test_docker_assets"
        image_name = "hello-world"

        bundle_cmd = [
            "assetkit", "bundle-docker-image", image_name, package_name,
            "--install", "--gen-assets-py", "--target-dir", str(tmp_path)
        ]
        result_bundle = subprocess.run(bundle_cmd, capture_output=True, text=True)
        assert result_bundle.returncode == 0, f"Bundle failed:\n{result_bundle.stderr}\n{result_bundle.stdout}"

        generated_package_path = tmp_path / package_name
        assert generated_package_path.exists(), "Asset package dir not created"
        assert (generated_package_path / "setup.cfg").exists()
        assert (generated_package_path / package_name / "resources" / "assets" / "image.tar").exists()

        load_cmd = ["assetkit", "load-docker", package_name, "image.tar"]
        result_load = subprocess.run(load_cmd, capture_output=True, text=True)
        assert result_load.returncode == 0, f"Load failed:\n{result_load.stderr}\n{result_load.stdout}"
        assert "Docker image loaded successfully" in result_load.stdout


@pytest.mark.integration
def test_bundle_docker_image_without_install():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        package_name = "noinstall_docker_assets"
        image_name = "hello-world"

        bundle_cmd = [
            "assetkit", "bundle-docker-image", image_name, package_name,
            "--gen-assets-py", "--target-dir", str(tmp_path)
        ]
        result = subprocess.run(bundle_cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"CLI failed:\n{result.stderr}\n{result.stdout}"

        generated_package_path = tmp_path / package_name
        assert generated_package_path.exists()
        assert (generated_package_path / package_name / "assets.py").exists()
        assert (generated_package_path / package_name / "resources" / "assets" / "image.tar").exists()
