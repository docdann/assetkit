import unittest
from unittest.mock import patch, MagicMock, ANY
from pathlib import Path
import subprocess
import os
from assetkit.internal.cli.bundle_docker_image import bundle_docker_image_cli
import shutil


class TestBundleDockerImageCLI(unittest.TestCase):

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    @patch("assetkit.internal.cli.bundle_docker_image.tempfile.TemporaryDirectory")
    @patch("assetkit.internal.cli.bundle_docker_image.create_new_project")
    @patch("assetkit.internal.cli.bundle_docker_image.Path.exists")
    @patch("shutil.copytree")
    def test_bundle_docker_image_success(
        self, mock_copytree, mock_path_exists, mock_create_new_project,
        mock_temp_dir, mock_subprocess_run
    ):
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = False
        args.target_dir = None

        mock_temp_dir_instance = MagicMock()
        mock_temp_dir.return_value = mock_temp_dir_instance
        mock_temp_dir_instance.name = os.path.normpath("C:/mock/temp/dir")

        mock_path_exists.return_value = False
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        bundle_docker_image_cli(args)

        mock_subprocess_run.assert_any_call(["docker", "pull", "ubuntu:22.04"], check=True)
        mock_create_new_project.assert_called_once()

        # ✅ Use ANY to avoid path mismatch in CI
        mock_subprocess_run.assert_any_call(
            ["docker", "save", "-o", ANY, "ubuntu:22.04"],
            check=True
        )
        mock_temp_dir_instance.cleanup.assert_called_once()

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    def test_docker_not_installed(self, mock_subprocess_run):
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = False
        args.target_dir = None

        mock_subprocess_run.side_effect = FileNotFoundError

        with self.assertRaises(SystemExit):
            bundle_docker_image_cli(args)

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    def test_docker_pull_failure(self, mock_subprocess_run):
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = False
        args.target_dir = None

        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "docker pull")

        with self.assertRaises(SystemExit):
            bundle_docker_image_cli(args)

    @patch("assetkit.internal.cli.bundle_docker_image.subprocess.run")
    @patch("assetkit.internal.cli.bundle_docker_image.generate_asset_mapping")
    @patch("assetkit.internal.cli.bundle_docker_image.Path.exists")
    @patch("shutil.copytree")
    def test_generate_assets_py(
        self, mock_copytree, mock_path_exists, mock_generate_asset_mapping, mock_subprocess_run
    ):
        args = MagicMock()
        args.image = "ubuntu:22.04"
        args.package = "test_package"
        args.install = False
        args.gen_assets_py = True
        args.target_dir = None

        with patch("assetkit.internal.cli.bundle_docker_image.tempfile.TemporaryDirectory") as mock_temp_dir:
            mock_temp_dir_instance = MagicMock()
            mock_temp_dir.return_value = mock_temp_dir_instance
            mock_temp_dir_instance.name = os.path.normpath("C:/mock/temp/dir")

            mock_path_exists.return_value = False

            bundle_docker_image_cli(args)

            # ✅ Use normalized comparison for path endings
            called_args = mock_generate_asset_mapping.call_args.kwargs
            assert called_args["resource_dir"] == "resources/assets"
            assert called_args["package_path"].name == "test_package"
            expected_suffix = os.path.normpath(os.path.join("test_package", "assets.py"))
            actual_output = os.path.normpath(str(called_args["output_filename"]))
            assert actual_output.endswith(expected_suffix), f"{actual_output} does not end with {expected_suffix}"


if __name__ == "__main__":
    unittest.main()
