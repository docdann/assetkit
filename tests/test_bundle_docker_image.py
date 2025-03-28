import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import subprocess
import os  # Import os for path normalization
from assetkit.internal.cli.bundle_docker_image import bundle_docker_image_cli
import shutil


class TestBundleDockerImageCLI(unittest.TestCase):

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    @patch("assetkit.internal.cli.bundle_docker_image.tempfile.TemporaryDirectory")
    @patch("assetkit.internal.cli.bundle_docker_image.create_new_project")
    @patch("assetkit.internal.cli.bundle_docker_image.Path.exists")  # Mock Path.exists
    @patch("shutil.copytree")  # Mock shutil.copytree
    def test_bundle_docker_image_success(self, mock_copytree, mock_path_exists, mock_create_new_project, mock_temp_dir, mock_subprocess_run):
        # Mock arguments
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = False
        args.target_dir = None

        # Mock temporary directory
        mock_temp_dir_instance = MagicMock()
        mock_temp_dir.return_value = mock_temp_dir_instance
        mock_temp_dir_instance.name = os.path.normpath("C:/mock/temp/dir")

        # Mock Path.exists to simulate the absence of the target directory
        mock_path_exists.return_value = False

        # Mock subprocess.run to simulate successful Docker commands
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        # Call the function
        bundle_docker_image_cli(args)

        # Assertions
        mock_subprocess_run.assert_any_call(["docker", "pull", "ubuntu:22.04"], check=True)
        mock_create_new_project.assert_called_once()
        mock_subprocess_run.assert_any_call(
            ["docker", "save", "-o", os.path.normpath("C:/mock/temp/dir/test_package/test_package/resources/assets/image.tar"), "ubuntu:22.04"],
            check=True
        )
        mock_temp_dir_instance.cleanup.assert_called_once()

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    def test_docker_not_installed(self, mock_subprocess_run):
        # Mock arguments
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = False
        args.target_dir = None

        # Simulate FileNotFoundError for Docker
        mock_subprocess_run.side_effect = FileNotFoundError

        # Call the function and assert SystemExit
        with self.assertRaises(SystemExit):
            bundle_docker_image_cli(args)

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    def test_docker_pull_failure(self, mock_subprocess_run):
        # Mock arguments
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = False
        args.target_dir = None

        # Simulate CalledProcessError for Docker pull
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "docker pull")

        # Call the function and assert SystemExit
        with self.assertRaises(SystemExit):
            bundle_docker_image_cli(args)

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    @patch("assetkit.internal.cli.bundle_docker_image.generate_asset_mapping")
    @patch("assetkit.internal.cli.bundle_docker_image.Path.exists")  # Mock Path.exists
    @patch("shutil.copytree")  # Mock shutil.copytree
    def test_generate_assets_py(self, mock_copytree, mock_path_exists, mock_generate_asset_mapping, mock_subprocess_run):
        # Mock arguments
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = True
        args.target_dir = None

        # Mock temporary directory
        with patch("assetkit.internal.cli.bundle_docker_image.tempfile.TemporaryDirectory") as mock_temp_dir:
            mock_temp_dir_instance = MagicMock()
            mock_temp_dir.return_value = mock_temp_dir_instance
            mock_temp_dir_instance.name = os.path.normpath("C:/mock/temp/dir")

            # Mock Path.exists to simulate the absence of the target directory
            mock_path_exists.return_value = False

            # Call the function
            bundle_docker_image_cli(args)

            # Assertions
            mock_generate_asset_mapping.assert_called_once_with(
                package_path=Path(os.path.normpath("C:/mock/temp/dir/test_package/test_package")),
                resource_dir="resources/assets",
                output_filename=os.path.normpath("C:/mock/temp/dir/test_package/test_package/assets.py")
            )


if __name__ == "__main__":
    unittest.main()
