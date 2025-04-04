import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from assetkit.cli.new import create_new_project

@pytest.fixture
def mock_args():
    return MagicMock(
        name="TestProject",
        add=["/path/to/asset1", "/path/to/asset2"],
        install=False,
        gen_assets_py=True,
        target_dir="."
    )

@patch("assetkit.cli.new.shutil.copytree")
@patch("assetkit.cli.new.Path.rglob")
@patch("assetkit.cli.new.Path.exists")
@patch("assetkit.cli.new.Path.mkdir")
@patch("assetkit.cli.new.subprocess.run")
@patch("assetkit.cli.new.generate_asset_mapping")
def test_create_new_project(
    mock_generate_asset_mapping,
    mock_subprocess_run,
    mock_mkdir,
    mock_exists,
    mock_rglob,
    mock_copytree,
    mock_args
):
    # Mock behaviors
    mock_exists.side_effect = lambda: False  # Simulate target directory does not exist
    mock_rglob.return_value = []  # Simulate no files in the template directory
    mock_generate_asset_mapping.return_value = None  # Simulate successful asset mapping generation
    mock_subprocess_run.return_value.returncode = 0  # Simulate successful subprocess call

    # Call the function
    create_new_project(mock_args)

    # Assertions
    mock_copytree.assert_called_once()  # Ensure template was copied
    mock_mkdir.assert_called()  # Ensure directories were created
    mock_generate_asset_mapping.assert_called_once()  # Ensure asset mapping was generated
    mock_subprocess_run.assert_not_called()  # Ensure no installation was attempted

@patch("assetkit.cli.new.shutil.copytree")
@patch("assetkit.cli.new.Path.exists")
def test_create_new_project_existing_directory(mock_exists, mock_copytree, mock_args):
    # Simulate target directory already exists
    mock_exists.side_effect = lambda: True

    # Call the function
    create_new_project(mock_args)

    # Assertions
    mock_copytree.assert_not_called()  # Ensure template was not copied
