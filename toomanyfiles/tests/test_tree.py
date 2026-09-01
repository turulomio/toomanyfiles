"""Unit tests for the TooManyFiles recursive tree execution."""

import json as std_json
from os import chdir, getcwd, path, makedirs
from tempfile import TemporaryDirectory
from toomanyfiles import tree as tmf_tree, toomanyfiles


def test_find_json_configs():
    """Verify recursive search finds all directories containing toomanyfiles.json with 3 config files."""
    with TemporaryDirectory() as tempdir:
        dir1 = path.join(tempdir, "subdir1")
        dir2 = path.join(tempdir, "subdir2", "nested")
        dir3 = path.join(tempdir, "subdir3", "deep", "level")
        dir_ignored = path.join(tempdir, "subdir_without_config")
        makedirs(dir1, exist_ok=True)
        makedirs(dir2, exist_ok=True)
        makedirs(dir3, exist_ok=True)
        makedirs(dir_ignored, exist_ok=True)

        with open(path.join(dir1, "toomanyfiles.json"), "w") as f:
            f.write("[]")
        with open(path.join(dir2, "toomanyfiles.json"), "w") as f:
            f.write("[]")
        with open(path.join(dir3, "toomanyfiles.json"), "w") as f:
            f.write("[]")

        found = tmf_tree.find_json_configs(tempdir)
        assert len(found) == 3
        assert dir1 in found
        assert dir2 in found
        assert dir3 in found
        assert dir_ignored not in found


def test_toomanyfiles_tree_three_json_execution():
    """Verify recursive execution of toomanyfiles_tree with 3 toomanyfiles.json configuration files."""
    with TemporaryDirectory() as tempdir:
        dir1 = path.join(tempdir, "backups")
        dir2 = path.join(tempdir, "logs", "app")
        dir3 = path.join(tempdir, "reports", "monthly", "data")
        makedirs(dir1, exist_ok=True)
        makedirs(dir2, exist_ok=True)
        makedirs(dir3, exist_ok=True)

        # Files in dir 1
        toomanyfiles.create_file(path.join(dir1, "20250101 Backup.xlsx"))
        toomanyfiles.create_file(path.join(dir1, "20250102 Backup.xlsx"))

        # Files in dir 2
        toomanyfiles.create_file(path.join(dir2, "20250201 App.log"))
        toomanyfiles.create_file(path.join(dir2, "20250202 App.log"))

        # Files in dir 3
        toomanyfiles.create_file(path.join(dir3, "20250301 Report.pdf"))
        toomanyfiles.create_file(path.join(dir3, "20250302 Report.pdf"))

        config1 = [{"time_pattern": "%Y%m%d", "too_young_to_delete": 0}]
        config2 = [{"time_pattern": "%Y%m%d", "too_young_to_delete": 0}]
        config3 = [{"time_pattern": "%Y%m%d", "too_young_to_delete": 0}]

        with open(path.join(dir1, "toomanyfiles.json"), "w") as f:
            std_json.dump(config1, f)
        with open(path.join(dir2, "toomanyfiles.json"), "w") as f:
            std_json.dump(config2, f)
        with open(path.join(dir3, "toomanyfiles.json"), "w") as f:
            std_json.dump(config3, f)

        # Dry run (pretend)
        results = tmf_tree.toomanyfiles_tree(tempdir, remove=False)
        assert len(results) == 3
        assert path.exists(path.join(dir1, "20250102 Backup.xlsx"))
        assert path.exists(path.join(dir2, "20250202 App.log"))
        assert path.exists(path.join(dir3, "20250302 Report.pdf"))

        # List mode
        list_results = tmf_tree.toomanyfiles_tree(tempdir, is_list=True)
        assert len(list_results) == 3

        # Actual removal
        tmf_tree.toomanyfiles_tree(tempdir, remove=True)
        assert path.exists(path.join(dir1, "20250101 Backup.xlsx"))
        assert not path.exists(path.join(dir1, "20250102 Backup.xlsx"))
        assert path.exists(path.join(dir2, "20250201 App.log"))
        assert not path.exists(path.join(dir2, "20250202 App.log"))
        assert path.exists(path.join(dir3, "20250301 Report.pdf"))
        assert not path.exists(path.join(dir3, "20250302 Report.pdf"))


def test_toomanyfiles_tree_empty():
    """Verify tree returns empty dict when no configuration files are found."""
    with TemporaryDirectory() as tempdir:
        res = tmf_tree.toomanyfiles_tree(tempdir)
        assert res == {}


def test_main_tree():
    """Verify main CLI invocations of tree module (--pretend, --list, --remove)."""
    old_cwd = getcwd()
    with TemporaryDirectory() as tempdir:
        try:
            chdir(tempdir)
            sub = path.join(tempdir, "sub")
            makedirs(sub, exist_ok=True)
            toomanyfiles.create_file(path.join(sub, "20250101 Backup.xlsx"))
            toomanyfiles.create_file(path.join(sub, "20250102 Backup.xlsx"))
            with open(path.join(sub, "toomanyfiles.json"), "w") as f:
                std_json.dump([{"time_pattern": "%Y%m%d", "too_young_to_delete": 0}], f)

            tmf_tree.main(["--pretend"])
            tmf_tree.main(["--list"])
            tmf_tree.main(["--remove"])
            assert path.exists(path.join(sub, "20250101 Backup.xlsx"))
            assert not path.exists(path.join(sub, "20250102 Backup.xlsx"))
        finally:
            chdir(old_cwd)
