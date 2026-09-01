"""Recursive tree execution of TooManyFiles JSON configurations.

Recursively discovers and executes all `toomanyfiles.json` configuration files
found in a directory tree.
"""

from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import init, Fore, Style
from gettext import translation
from importlib.resources import files
from os import getcwd, walk, path
from pydicts import colors
from tqdm import tqdm
from toomanyfiles import json as tmf_json

try:
    t = translation('toomanyfiles', files("toomanyfiles/") / 'locale')
    _ = t.gettext
except:
    _ = str


def find_json_configs(root_directory):
    """Recursively find all directories containing a toomanyfiles.json file.

    Args:
        root_directory (str): Root directory path to start search.

    Returns:
        list[str]: Sorted list of directory paths containing toomanyfiles.json.
    """
    config_dirs = []
    for dirpath, _, filenames in walk(root_directory):
        if tmf_json.DEFAULT_CONFIG_FILENAME in filenames:
            config_dirs.append(dirpath)
    config_dirs.sort()
    return config_dirs


def toomanyfiles_tree(root_directory=None, remove=False, is_list=False):
    """Recursively execute toomanyfiles_json in all directories with toomanyfiles.json.

    Args:
        root_directory (str, optional): Root directory to search. Defaults to current working directory.
        remove (bool, optional): If True, deletes files; if False, simulates. Defaults to False.
        is_list (bool, optional): If True, lists files matched and ignored. Defaults to False.

    Returns:
        dict[str, list]: Mapping of directory paths to their toomanyfiles_json execution results.
    """
    if root_directory is None:
        root_directory = getcwd()

    config_dirs = find_json_configs(root_directory)
    if not config_dirs:
        print(Fore.YELLOW + _("No '{}' files found in directory tree under '{}'.").format(tmf_json.DEFAULT_CONFIG_FILENAME, root_directory) + Style.RESET_ALL)
        return {}

    print(colors.magenta(_("Found {} configuration directory(ies) under '{}':")).format(len(config_dirs), root_directory))
    for d in config_dirs:
        print(f"  * {d}")
    print()

    results = {}
    for d in tqdm(config_dirs, desc=_("Processing directories")):
        print(Style.BRIGHT + Fore.CYAN + ">>> " + _("Processing directory: {}").format(d) + Style.RESET_ALL)
        results[d] = tmf_json.toomanyfiles_json(d, remove=remove, is_list=is_list)
        print()
    return results


def main(arguments=None):
    """CLI entry point for toomanyfiles_tree.

    Parses command-line arguments and executes toomanyfiles recursively for all toomanyfiles.json files found.

    Args:
        arguments (list[str], optional): List of command-line arguments.
            If None, arguments are read from sys.argv. Defaults to None.
    """
    from .__init__ import __version__, __versiondate__

    parser = ArgumentParser(
        prog='toomanyfiles_tree',
        description=_('Recursively search and execute all toomanyfiles.json configuration files in a directory tree'),
        epilog=_("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year),
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('--version', action='version', version=__version__)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--remove', help=_("Removes files permanently according to all toomanyfiles.json found in tree"), action="store_true", default=False)
    group.add_argument('--pretend', help=_("Makes a simulation and doesn't remove files according to all toomanyfiles.json found in tree"), action="store_true", default=False)
    group.add_argument('--list', help=_("List files included and excluded for each toomanyfiles.json found in tree"), action="store_true", default=False)

    args = parser.parse_args(arguments)

    init(autoreset=True)
    if args.remove:
        toomanyfiles_tree(getcwd(), remove=True)
    elif args.pretend:
        toomanyfiles_tree(getcwd(), remove=False)
    elif args.list:
        toomanyfiles_tree(getcwd(), is_list=True)
