"""JSON configuration management and execution for TooManyFiles.

Provides functions to create default configuration files and execute TooManyFiles
retention rules based on a list of configurations defined in a JSON file.
"""

from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import init, Fore, Style
from gettext import translation
from importlib.resources import files
import json as std_json
from os import getcwd, path
from pydicts import lod, colors
from sys import exit
from toomanyfiles import types, toomanyfiles

try:
    t = translation('toomanyfiles', files("toomanyfiles") / 'locale', fallback=True)
    _ = t.gettext
except:
    _ = str


DEFAULT_CONFIG_FILENAME = "toomanyfiles.json"

DEFAULT_JSON_CONFIG = [
    {
        "time_pattern": "%Y%m%d %H%M",
        "file_patterns": [],
        "too_young_to_delete": 30,
        "max_files_to_store": 100000000,
        "remove_mode": "RemainFirstInMonth",
        "disable_log": False
    }
]


def create_json_config(directory=None):
    """Create a default toomanyfiles.json configuration file in the specified directory.

    Args:
        directory (str, optional): Target directory. Defaults to current working directory.

    Returns:
        bool: True if created, False if file already exists.
    """
    if directory is None:
        directory = getcwd()
    config_file = path.join(directory, DEFAULT_CONFIG_FILENAME)
    if path.exists(config_file):
        print(Fore.YELLOW + _("Configuration file '{}' already exists.").format(config_file) + Style.RESET_ALL)
        return False

    with open(config_file, "w", encoding="utf-8") as f:
        std_json.dump(DEFAULT_JSON_CONFIG, f, indent=4, ensure_ascii=False)
        f.write("\n")

    print(Fore.GREEN + _("Configuration file '{}' created successfully.").format(config_file) + Style.RESET_ALL)
    return True


def toomanyfiles_json(directory=None, remove=False, is_list=False, show_output=True):
    """Run toomanyfiles operations according to configuration in toomanyfiles.json.

    Args:
        directory (str, optional): Target directory. Defaults to current working directory.
        remove (bool, optional): If True, deletes files; if False, simulates (dry-run). Defaults to False.
        is_list (bool, optional): If True, lists files matched and ignored. Defaults to False.
        show_output (bool, optional): If True, displays console output. Defaults to True.

    Returns:
        list[tuple]: List of results for each configuration item.
    """
    if directory is None:
        directory = getcwd()
    config_file = path.join(directory, DEFAULT_CONFIG_FILENAME)
    if not path.exists(config_file):
        print(Fore.RED + _("Configuration file '{}' not found. Use --create to create one.").format(config_file) + Style.RESET_ALL)
        exit(types.ExitCodes.ArgumentError)

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            configs = std_json.load(f)
    except Exception as e:
        print(Fore.RED + _("Error reading configuration file '{}': {}").format(config_file, e) + Style.RESET_ALL)
        exit(types.ExitCodes.ArgumentError)

    if not isinstance(configs, list):
        print(Fore.RED + _("Configuration file '{}' must contain a JSON array/list.").format(config_file) + Style.RESET_ALL)
        exit(types.ExitCodes.ArgumentError)

    results = []
    for index, config in enumerate(configs, 1):
        if not isinstance(config, dict):
            print(Fore.RED + _("Configuration item #{} is not a JSON object/dict.").format(index) + Style.RESET_ALL)
            exit(types.ExitCodes.ArgumentError)

        time_pattern = config.get("time_pattern", "%Y%m%d %H%M")
        file_patterns = config.get("file_patterns", [])
        too_young_to_delete = config.get("too_young_to_delete", 30)
        max_files_to_store = config.get("max_files_to_store", 100000000)
        remove_mode_str = config.get("remove_mode", "RemainFirstInMonth")
        remove_mode = types.RemoveMode.from_string(remove_mode_str)
        disable_log = config.get("disable_log", False)

        if is_list:
            files_to_process, files_to_ignore = toomanyfiles.lod_read_directory(directory, time_pattern, file_patterns)
            processed = toomanyfiles.lod_process_directory(files_to_process, remove_mode, too_young_to_delete, max_files_to_store)

            processed = lod.lod_order_by(processed, "filename")
            files_to_ignore = lod.lod_order_by(files_to_ignore, "filename")

            if show_output:
                print(colors.magenta("=== " + _("CONFIGURATION #{}: FILES TO PROCESS").format(index) + " ==="))
                toomanyfiles.print_with_type(processed)
                print()
                print(colors.magenta("=== " + _("CONFIGURATION #{}: FILES IGNORED").format(index) + " ==="))
                toomanyfiles.print_with_type(files_to_ignore)
            results.append((processed, files_to_ignore))
        else:
            res = toomanyfiles.toomanyfiles(
                directory,
                remove=remove,
                time_pattern=time_pattern,
                file_patterns=file_patterns,
                too_young_to_delete=too_young_to_delete,
                max_files_to_store=max_files_to_store,
                remove_mode=remove_mode,
                disable_log=disable_log,
                show_output=show_output
            )
            results.append(res)
    return results


def main(arguments=None):
    """CLI entry point for toomanyfiles_json.

    Parses command-line arguments and executes toomanyfiles operations based on toomanyfiles.json.

    Args:
        arguments (list[str], optional): List of command-line arguments.
            If None, arguments are read from sys.argv. Defaults to None.
    """
    from .__init__ import __version__, __versiondate__

    parser = ArgumentParser(
        prog='toomanyfiles_json',
        description=_('Search date and time patterns to delete unnecessary files or directories using a JSON configuration file'),
        epilog=_("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year),
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('--version', action='version', version=__version__)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create', help=_("Creates a default toomanyfiles.json configuration file in current directory"), action="store_true", default=False)
    group.add_argument('--remove', help=_("Removes files permanently according to toomanyfiles.json"), action="store_true", default=False)
    group.add_argument('--pretend', help=_("Makes a simulation and doesn't remove files according to toomanyfiles.json"), action="store_true", default=False)
    group.add_argument('--list', help=_("List files included and excluded for each configuration in toomanyfiles.json"), action="store_true", default=False)

    args = parser.parse_args(arguments)

    init(autoreset=True)
    if args.create:
        create_json_config(getcwd())
    elif args.remove:
        toomanyfiles_json(getcwd(), remove=True)
    elif args.pretend:
        toomanyfiles_json(getcwd(), remove=False)
    elif args.list:
        toomanyfiles_json(getcwd(), is_list=True)
