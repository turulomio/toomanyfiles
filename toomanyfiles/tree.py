"""Recursive tree execution of TooManyFiles JSON configurations.

Recursively discovers and executes all `TooManyFiles.json` configuration files
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
    t = translation('toomanyfiles', files("toomanyfiles") / 'locale', fallback=True)
    _ = t.gettext
except:
    _ = str


def find_json_configs(root_directory):
    """Recursively find all directories containing a TooManyFiles.json file.

    Args:
        root_directory (str): Root directory path to start search.

    Returns:
        list[str]: Sorted list of directory paths containing TooManyFiles.json.
    """
    config_dirs = []
    for dirpath, _, filenames in walk(root_directory):
        if tmf_json.DEFAULT_CONFIG_FILENAME in filenames:
            config_dirs.append(dirpath)
    config_dirs.sort()
    return config_dirs


def toomanyfiles_tree(root_directory=None, remove=False, is_list=False, show_output=False):
    """Recursively execute toomanyfiles_json in all directories with TooManyFiles.json.

    Args:
        root_directory (str, optional): Root directory to search. Defaults to current working directory.
        remove (bool, optional): If True, deletes files; if False, simulates. Defaults to False.
        is_list (bool, optional): If True, lists files matched and ignored. Defaults to False.
        show_output (bool, optional): If True, displays detailed output for each directory. Defaults to False.

    Returns:
        dict[str, list]: Mapping of directory paths to their toomanyfiles_json execution results.
    """
    if root_directory is None:
        root_directory = getcwd()

    config_dirs = find_json_configs(root_directory)
    if not config_dirs:
        print(Fore.YELLOW + _("No '{}' files found in directory tree under '{}'.").format(tmf_json.DEFAULT_CONFIG_FILENAME, root_directory) + Style.RESET_ALL)
        return {}

    if show_output:
        print(colors.magenta(_("Found {} configuration directory(ies) under '{}':")).format(len(config_dirs), root_directory))
        for d in config_dirs:
            print(f"  * {d}")
        print()

    results = {}
    pbar = tqdm(config_dirs)
    for d in pbar:
        config_file = path.join(d, tmf_json.DEFAULT_CONFIG_FILENAME)
        pbar.set_description(config_file)
        if show_output:
            print(Style.BRIGHT + Fore.CYAN + ">>> " + _("Processing directory: {}").format(d) + Style.RESET_ALL)
        results[d] = tmf_json.toomanyfiles_json(d, remove=remove, is_list=is_list, show_output=show_output)
        if show_output:
            print()
    return results


def main(arguments=None):
    """CLI entry point for toomanyfiles_tree.

    Parses command-line arguments and executes toomanyfiles recursively for all TooManyFiles.json files found.

    Args:
        arguments (list[str], optional): List of command-line arguments.
            If None, arguments are read from sys.argv. Defaults to None.
    """
    from .__init__ import __version__, __versiondate__

    parser = ArgumentParser(
        prog='toomanyfiles_tree',
        description=_('Recursively search and execute all TooManyFiles.json configuration files in a directory tree'),
        epilog=_("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year),
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('--version', action='version', version=__version__)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--remove', help=_("Removes files permanently according to all TooManyFiles.json found in tree"), action="store_true", default=False)
    group.add_argument('--pretend', help=_("Makes a simulation and doesn't remove files according to all TooManyFiles.json found in tree"), action="store_true", default=False)
    group.add_argument('--list', help=_("List files included and excluded for each TooManyFiles.json found in tree"), action="store_true", default=False)

    parser.add_argument('--show_output', help=_("Shows detailed output for each configuration"), action="store_true", default=False)

    args = parser.parse_args(arguments)

    init(autoreset=True)
    if args.remove:
        toomanyfiles_tree(getcwd(), remove=True, show_output=args.show_output)
    elif args.pretend:
        toomanyfiles_tree(getcwd(), remove=False, show_output=args.show_output)
    elif args.list:
        toomanyfiles_tree(getcwd(), is_list=True, show_output=args.show_output)
