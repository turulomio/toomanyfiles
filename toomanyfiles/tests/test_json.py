"""Unit tests for the TooManyFiles JSON configuration and CLI functionality."""

import json as std_json
from os import chdir, getcwd, path
import pytest
from tempfile import TemporaryDirectory
from toomanyfiles import json as tmf_json
from toomanyfiles import toomanyfiles


def test_create_json_config():
    """Verify create_json_config creates a valid JSON configuration and handles duplicate creation."""
    with TemporaryDirectory() as tempdir:
        config_path = path.join(tempdir, "toomanyfiles.json")
        assert not path.exists(config_path)

        res = tmf_json.create_json_config(tempdir)
        assert res is True
        assert path.exists(config_path)

        with open(config_path, "r", encoding="utf-8") as f:
            data = std_json.load(f)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["time_pattern"] == "%Y%m%d %H%M"

        # Calling again should return False and not fail
        res2 = tmf_json.create_json_config(tempdir)
        assert res2 is False


def test_toomanyfiles_json_execution():
    """Verify toomanyfiles_json processes 3 configuration entries in a directory."""
    with TemporaryDirectory() as tempdir:
        toomanyfiles.create_file(f"{tempdir}/20250101 Backup.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250102 Backup.xlsx")
        toomanyfiles.create_file(f"{tempdir}/20250201 Log.txt")
        toomanyfiles.create_file(f"{tempdir}/20250202 Log.txt")
        toomanyfiles.create_file(f"{tempdir}/20250301 Report.pdf")
        toomanyfiles.create_file(f"{tempdir}/20250302 Report.pdf")

        config = [
            {
                "time_pattern": "%Y%m%d",
                "file_patterns": ["Backup"],
                "too_young_to_delete": 0
            },
            {
                "time_pattern": "%Y%m%d",
                "file_patterns": ["Log"],
                "too_young_to_delete": 0
            },
            {
                "time_pattern": "%Y%m%d",
                "file_patterns": ["Report"],
                "too_young_to_delete": 0
            }
        ]
        with open(path.join(tempdir, "toomanyfiles.json"), "w", encoding="utf-8") as f:
            std_json.dump(config, f)

        # Dry run (pretend)
        results = tmf_json.toomanyfiles_json(tempdir, remove=False)
        assert len(results) == 3
        assert path.exists(f"{tempdir}/20250102 Backup.xlsx")
        assert path.exists(f"{tempdir}/20250202 Log.txt")
        assert path.exists(f"{tempdir}/20250302 Report.pdf")

        # List mode
        list_results = tmf_json.toomanyfiles_json(tempdir, is_list=True)
        assert len(list_results) == 3

        # Actual removal
        tmf_json.toomanyfiles_json(tempdir, remove=True)
        assert path.exists(f"{tempdir}/20250101 Backup.xlsx")
        assert not path.exists(f"{tempdir}/20250102 Backup.xlsx")
        assert path.exists(f"{tempdir}/20250201 Log.txt")
        assert not path.exists(f"{tempdir}/20250202 Log.txt")
        assert path.exists(f"{tempdir}/20250301 Report.pdf")
        assert not path.exists(f"{tempdir}/20250302 Report.pdf")


def test_toomanyfiles_json_errors():
    """Verify toomanyfiles_json exits properly on invalid JSON or missing configuration."""
    with TemporaryDirectory() as tempdir:
        # Missing config
        with pytest.raises(SystemExit):
            tmf_json.toomanyfiles_json(tempdir)

        # Invalid JSON syntax
        with open(path.join(tempdir, "toomanyfiles.json"), "w") as f:
            f.write("{ invalid json")
        with pytest.raises(SystemExit):
            tmf_json.toomanyfiles_json(tempdir)

        # Not a list
        with open(path.join(tempdir, "toomanyfiles.json"), "w") as f:
            f.write('{"key": "value"}')
        with pytest.raises(SystemExit):
            tmf_json.toomanyfiles_json(tempdir)

        # Item not a dict
        with open(path.join(tempdir, "toomanyfiles.json"), "w") as f:
            f.write('[123]')
        with pytest.raises(SystemExit):
            tmf_json.toomanyfiles_json(tempdir)


def test_main_json():
    """Verify main CLI invocations of json module (--create, --pretend, --remove, --list)."""
    old_cwd = getcwd()
    with TemporaryDirectory() as tempdir:
        try:
            chdir(tempdir)
            toomanyfiles.create_file(f"{tempdir}/20250101 Backup.xlsx")
            toomanyfiles.create_file(f"{tempdir}/20250102 Backup.xlsx")

            # Create default config
            tmf_json.main(["--create"])
            assert path.exists("toomanyfiles.json")

            # Pretend
            tmf_json.main(["--pretend"])

            # List
            tmf_json.main(["--list"])

            # Remove
            tmf_json.main(["--remove"])
        finally:
            chdir(old_cwd)
