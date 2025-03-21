import tempfile
import shutil
from pathlib import Path
from assetkit.cli.scaffold import scaffold_project, TEMPLATE_ROOT

def test_scaffold_project_creates_target_with_placeholder_replacement(monkeypatch):
    tmpdir = tempfile.mkdtemp()
    try:
        tmp_path = Path(tmpdir)
        app_type = "mlkit"
        project_name = "my_app"

        template_path = TEMPLATE_ROOT / app_type
        template_path.mkdir(parents=True, exist_ok=True)
        (template_path / "file.txt").write_text("Hello {{PROJECT_NAME}}!")

        monkeypatch.chdir(tmp_path)
        scaffold_project(app_type, project_name)

        target_dir = tmp_path / project_name
        assert target_dir.exists()
        assert (target_dir / "file.txt").exists()
        content = (target_dir / "file.txt").read_text()
        assert content.strip() == "Hello my_app!"
    finally:
        try:
            shutil.rmtree(tmpdir)
        except PermissionError:
            print("⚠ Skipped cleanup due to file lock.")

def test_scaffold_project_skips_missing_template(monkeypatch):
    tmpdir = tempfile.mkdtemp()
    try:
        tmp_path = Path(tmpdir)
        app_type = "nonexistent"
        project_name = "ghost_app"

        monkeypatch.chdir(tmp_path)
        scaffold_project(app_type, project_name)

        assert not (tmp_path / project_name).exists()
    finally:
        try:
            shutil.rmtree(tmpdir)
        except PermissionError:
            print("⚠ Skipped cleanup due to file lock.")

def test_scaffold_project_skips_binary_files(monkeypatch):
    tmpdir = tempfile.mkdtemp()
    try:
        tmp_path = Path(tmpdir)
        app_type = "mlkit_binary"
        project_name = "binary_app"

        template_path = TEMPLATE_ROOT / app_type
        template_path.mkdir(parents=True, exist_ok=True)
        with open(template_path / "image.png", "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")

        monkeypatch.chdir(tmp_path)
        scaffold_project(app_type, project_name)

        target_path = tmp_path / project_name / "image.png"
        assert target_path.exists()
        with open(target_path, "rb") as f:
            assert f.read().startswith(b"\x89PNG")
    finally:
        try:
            shutil.rmtree(tmpdir)
        except PermissionError:
            print("⚠ Skipped cleanup due to file lock.")