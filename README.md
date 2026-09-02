# TooManyFiles

[![Tests](https://github.com/turulomio/toomanyfiles/actions/workflows/pytest.yml/badge.svg)](https://github.com/turulomio/toomanyfiles/actions/workflows/pytest.yml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/toomanyfiles)](https://pypi.org/project/toomanyfiles/)

## Links

Source code & Development: https://github.com/turulomio/toomanyfiles/

## Installation
`pip install toomanyfiles`

If you use Gentoo you can find a ebuild in https://github.com/turulomio/myportage/tree/master/app-admin/toomanyfiles

## Description
This package provides three commands:
* `toomanyfiles`: Removes files and directories matching date and time patterns according to retention rules passed via CLI arguments.
* `toomanyfiles_json`: Reads configuration from a `TooManyFiles.json` file in the current directory containing a list of configuration objects, and executes retention rules for each configuration in the current directory.
* `toomanyfiles_tree`: Recursively finds and executes all `TooManyFiles.json` configuration files in a directory tree.

## Usage

### toomanyfiles
<img src="https://raw.githubusercontent.com/turulomio/toomanyfiles/master/doc/command.gif?raw=true" width="100%"></img>

You can see this animated gif to learn how to use `toomanyfiles`:

<img src="https://raw.githubusercontent.com/turulomio/toomanyfiles/master/doc/howto.gif?raw=true" width="100%"></img>

### toomanyfiles_json
`toomanyfiles_json` allows defining multiple `toomanyfiles` configurations in a single `TooManyFiles.json` file. When executed, each configuration in the list is processed sequentially in order in the current directory.

You can initialize a default configuration file in the current directory:
```bash
toomanyfiles_json --create
```

This creates a `TooManyFiles.json` containing a list of configurations. You can add as many configurations as needed to execute multiple retention policies in order:
```json
[
    {
        "time_pattern": "%Y%m%d %H%M",
        "file_patterns": [".tar.gz", "backup"],
        "too_young_to_delete": 30,
        "max_files_to_store": 100000000,
        "remove_mode": "RemainFirstInMonth",
        "disable_log": false
    },
    {
        "time_pattern": "%Y%m%d",
        "file_patterns": [".log"],
        "too_young_to_delete": 7,
        "max_files_to_store": 50,
        "remove_mode": "RemainFirstInMonth",
        "disable_log": false
    }
]
```

To simulate (dry-run) without removing files:
```bash
toomanyfiles_json --pretend
```

To list included and excluded files:
```bash
toomanyfiles_json --list
```

To execute file deletion:
```bash
toomanyfiles_json --remove
```

You can see this animated gif to learn how to use `toomanyfiles_json`:

<img src="https://raw.githubusercontent.com/turulomio/toomanyfiles/master/doc/json.gif?raw=true" width="100%"></img>

### toomanyfiles_tree
`toomanyfiles_tree` recursively discovers all `TooManyFiles.json` files within the current directory tree and executes them.

To simulate (dry-run) across all found configuration files:
```bash
toomanyfiles_tree --pretend
```

To list files across all found configuration files:
```bash
toomanyfiles_tree --list
```

To execute deletion across all found configuration files:
```bash
toomanyfiles_tree --remove
```

To display detailed output for each configuration instead of the progress bar:
```bash
toomanyfiles_tree --pretend --show_output
```

You can see this animated gif to learn how to use `toomanyfiles_tree`:

<img src="https://raw.githubusercontent.com/turulomio/toomanyfiles/master/doc/tree.gif?raw=true" width="100%"></img>
