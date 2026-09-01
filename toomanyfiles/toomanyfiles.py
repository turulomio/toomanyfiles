"""Core logic and CLI interface for TooManyFiles.

Provides functions to scan directories, parse timestamps from filenames, determine
file retention and deletion status based on configurable retention rules, and perform
actual file or directory removal.
"""

from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from gettext import translation
from importlib.resources import files
from os import getcwd, listdir, sep, path, remove as os_remove, makedirs
from pydicts import lod, colors
from shutil import rmtree
from sys import exit
from toomanyfiles import types

try:
    t = translation('toomanyfiles', files("toomanyfiles") / 'locale', fallback=True)
    _ = t.gettext
except:
    _ = str


def datetime_in_basename(basename, pattern):
    """Find a datetime pattern in a filename's basename.

    Iterates through substrings of ``basename`` to find a matching ``strptime`` format.

    Args:
        basename (str): Base filename (without parent directory path).
        pattern (str): Datetime format string compatible with ``strptime`` (e.g. '%Y%m%d %H%M').

    Returns:
        datetime | None: Parsed datetime object if a match is found, otherwise None.
    """
    length = len(datetime.now().strftime(pattern))  # Len of the value of the pattern

    if len(basename) < len(pattern):
        return None
    for i in range(len(basename) - length + 1):
        s = basename[i:length + i]
        try:
            dt = datetime.strptime(s, pattern)
            return dt
        except:
            pass
    return None


def header_string(lod_, directory, time_pattern, file_patterns, color=False):
    """Generate the formatted header summary string.

    Args:
        lod_ (list[dict]): List of dictionaries representing files to process.
        directory (str): Path to the target directory.
        time_pattern (str): The datetime format pattern used.
        file_patterns (list[str]): List of substring filter patterns required in filenames.
        color (bool, optional): Whether to apply ANSI color formatting. Defaults to False.

    Returns:
        str: Formatted header message.
    """
    if color is True:
        return _("{} TooManyFiles in {} detected {} files with time pattern {} and filename patterns {}").format(
            Style.BRIGHT + str(datetime.now()) + Style.RESET_ALL,
            Style.BRIGHT + Fore.YELLOW + directory + Style.RESET_ALL,
            Style.BRIGHT + Fore.GREEN + str(len(lod_)) + Style.RESET_ALL,
            Fore.YELLOW + time_pattern + Style.RESET_ALL,
            Fore.YELLOW + str(file_patterns) + Style.RESET_ALL,
        )
    else:
        return _("{} TooManyFiles in {} detected {} files with time pattern {} and filename patterns {}").format(
            datetime.now(), directory, len(lod_), time_pattern, str(file_patterns)
        )


def console_output(lod_, directory, remove, time_pattern, file_patterns, too_young_to_delete, max_files_to_store):
    """Print the summary report and status of files to the console.

    Args:
        lod_ (list[dict]): List of dictionaries representing processed files.
        directory (str): Path of the processed directory.
        remove (bool): True if removal was executed, False if dry-run (pretend).
        time_pattern (str): Datetime format pattern used.
        file_patterns (list[str]): List of required filename patterns.
        too_young_to_delete (int): Number of most recent files protected from deletion.
        max_files_to_store (int): Maximum number of files permitted to be kept.
    """
    def one_line_status():
        """Return a colored single-line string with status codes (R, D, Y, O) for all files.

        Returns:
            str: Colorized status line.
        """
        s = ""
        for o in lod_:
            if o["status"] == types.FileStatus.Remain:
                s = s + "{}".format(Fore.GREEN + _("R") + Fore.RESET)
            elif o["status"] == types.FileStatus.Delete:
                s = s + "{}".format(Fore.RED + _("D") + Fore.RESET)
            elif o["status"] == types.FileStatus.TooYoungToDelete:
                s = s + "{}".format(Fore.MAGENTA + _("Y") + Style.RESET_ALL)
            elif o["status"] == types.FileStatus.OverMaxFiles:
                s = s + "{}".format(Fore.YELLOW + _("O") + Style.RESET_ALL)
        return s

    print(header_string(lod_, directory, time_pattern, file_patterns, color=True))
    if len(lod_) == 0:
        return
    print(_("   Parameters: Too young to delete:"), too_young_to_delete, _("Max files to store:"), max_files_to_store)

    print(one_line_status())

    n_remain = lod.lod_count(lod_, lambda d, index: d["status"] == types.FileStatus.Remain)
    n_delete = lod.lod_count(lod_, lambda d, index: d["status"] == types.FileStatus.Delete)
    n_young = lod.lod_count(lod_, lambda d, index: d["status"] == types.FileStatus.TooYoungToDelete)
    n_over = lod.lod_count(lod_, lambda d, index: d["status"] == types.FileStatus.OverMaxFiles)
    if remove is False:
        print(_("Files status pretending:"))
        result = _("So, {} files will be deleted and {} will be kept when you use --remove parameter.").format(
            Fore.YELLOW + str(n_delete + n_over) + Style.RESET_ALL,
            Fore.YELLOW + str(n_remain + n_young) + Style.RESET_ALL
        )
    else:
        print(_("File status removing:"))
        result = _("So, {} files have been deleted and {} files have been kept.").format(
            Fore.YELLOW + str(n_delete + n_over) + Style.RESET_ALL,
            Fore.YELLOW + str(n_remain + n_young) + Style.RESET_ALL
        )
    print("  * {} [{}]: {}".format(_("Remains"), Fore.GREEN + _("R") + Style.RESET_ALL, n_remain))
    print("  * {} [{}]: {}".format(_("Delete"), Fore.RED + _("D") + Style.RESET_ALL, n_delete))
    print("  * {} [{}]: {}".format(_("Too young to delete"), Fore.MAGENTA + _("Y") + Style.RESET_ALL, n_young))
    print("  * {} [{}]: {}".format(_("Over max files"), Fore.YELLOW + _("O") + Style.RESET_ALL, n_over))
    print(result)


def create_file(filename):
    """Create an empty file and its parent directories if they do not exist.

    Args:
        filename (str): Full path to the file to create.
    """
    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, "w"):
        pass


def create_directory(directory):
    """Create a directory and any intermediate parent directories if they do not exist.

    Args:
        directory (str): Path of the directory to create.
    """
    makedirs(directory, exist_ok=True)


def lod_read_directory(directory, time_pattern, file_patterns):
    """Scan a directory and categorize entries into processable and ignored files.

    Args:
        directory (str): Path of the directory to scan.
        time_pattern (str): Datetime format pattern to search in filenames.
        file_patterns (list[str]): Substring patterns that filenames must contain.

    Returns:
        tuple[list[dict], list[dict]]: A tuple containing:
            - files_to_process: List of file dictionaries matching the time and file patterns, sorted chronologically.
            - files_to_ignore: List of file dictionaries that did not match, with reason descriptions.
    """
    files_to_process = []
    files_to_ignore = []
    for basename in listdir(directory):
        filename = directory + sep + basename
        isdir = path.isdir(filename)
        type = _("Directory") if isdir else _("File")
        dt = datetime_in_basename(basename, time_pattern)
        if dt is not None:
            # Selects if matches all file_patterns
            found_file_patterns = True
            for fp in file_patterns:
                if fp not in filename:
                    found_file_patterns = False
                    break

            if found_file_patterns:
                files_to_process.append({
                    "filename": filename,
                    "dt": dt,
                    "status": None,
                    "type": type
                })
            else:
                files_to_ignore.append({
                    "filename": filename,
                    "reason": _("File patterns weren't found"),
                    "type": type
                })
        else:
            files_to_ignore.append({
                "filename": filename,
                "reason": _("Time pattern wasn't found"),
                "type": type
            })

    files_to_process = lod.lod_order_by(files_to_process, "dt")
    return files_to_process, files_to_ignore


def lod_process_directory(lod_, remove_mode, too_young_to_delete, max_files_to_store):
    """Assign file statuses (Remain, Delete, TooYoungToDelete, OverMaxFiles) to entries.

    Args:
        lod_ (list[dict]): Chronologically ordered list of file dictionaries.
        remove_mode (int): Removal strategy mode from ``types.RemoveMode``.
        too_young_to_delete (int): Number of most recent files to protect.
        max_files_to_store (int): Maximum number of remaining files to keep.

    Returns:
        list[dict]: The updated list of file dictionaries with assigned statuses.
    """
    if too_young_to_delete > max_files_to_store:
        print(Fore.RED + _("The number of files too young to delete can't be bigger than the maximum number of files to store") + Style.RESET_ALL)
        exit(types.ExitCodes.YoungGTMax)
    # Process lod
    aux = []  # Strings containing YYYYMM
    if remove_mode == types.RemoveMode.RemainFirstInMonth:
        # Set status too_young
        if len(lod_) >= too_young_to_delete:
            for o in lod_[len(lod_) - too_young_to_delete:len(lod_)]:
                o["status"] = types.FileStatus.TooYoungToDelete
        else:
            for o in lod_:
                o["status"] = types.FileStatus.TooYoungToDelete

        # Leaving first in month
        if len(lod_) >= too_young_to_delete:
            for o in lod_[0:len(lod_) - too_young_to_delete]:
                tuple_ym = (o["dt"].year, o["dt"].month)
                if tuple_ym not in aux:
                    o["status"] = types.FileStatus.Remain
                    aux.append(tuple_ym)
                else:
                    o["status"] = types.FileStatus.Delete

        # Changes remaining files to overmaxfiles
        remaining = 0
        for o in reversed(lod_):
            if o["status"] == types.FileStatus.Remain:
                if remaining >= max_files_to_store - too_young_to_delete:
                    o["status"] = types.FileStatus.OverMaxFiles
                else:
                    remaining += 1

    elif remove_mode == types.RemoveMode.RemainLastInMonth:
        print(_("Not developed yet"))
        exit(types.ExitCodes.NotDeveloped)

    return lod_


def write_log(lod_, directory, time_pattern, file_patterns):
    """Append the execution header and deleted file actions to TooManyFiles.log.

    Args:
        lod_ (list[dict]): Processed file dictionaries with assigned statuses.
        directory (str): Target directory path.
        time_pattern (str): Datetime format pattern used.
        file_patterns (list[str]): Filename patterns used.
    """
    s = header_string(lod_, directory, time_pattern, file_patterns, color=False) + "\n"
    for o in lod_:
        if o["status"] == types.FileStatus.Delete:
            s = s + "{} >>> {}\n".format(o["filename"], _("Delete"))
        elif o["status"] == types.FileStatus.OverMaxFiles:
            s = s + "{} >>> {}\n".format(o["filename"], _("Over max number of files"))
    with open("TooManyFiles.log", "a") as f:
        f.write(s)


def toomanyfiles(directory, remove, time_pattern="%Y%m%d %H%M", file_patterns=[], too_young_to_delete=30, max_files_to_store=100000000, remove_mode=types.RemoveMode.RemainFirstInMonth, disable_log=False):
    """Programmatic entry point to analyze and optionally remove obsolete files or directories.

    Scans the specified directory for files matching date/time and name patterns,
    applies retention rules, displays console output, logs operations, and deletes
    files when `remove` is set to True.

    Args:
        directory (str): Directory path to scan and clean.
        remove (bool): If True, deletes files marked for deletion. If False, only simulates (dry run).
        time_pattern (str, optional): Datetime format pattern (strptime). Defaults to "%Y%m%d %H%M".
        file_patterns (list[str], optional): Substrings required in filenames. Defaults to [].
        too_young_to_delete (int, optional): Count of most recent files to keep. Defaults to 30.
        max_files_to_store (int, optional): Maximum number of files to keep. Defaults to 100000000.
        remove_mode (int, optional): Retention strategy from `types.RemoveMode`. Defaults to `RemainFirstInMonth`.
        disable_log (bool, optional): If True, suppresses appending to TooManyFiles.log. Defaults to False.

    Returns:
        tuple[list[dict], list[dict]]: A tuple containing (processed_files, ignored_files).
    """
    files_to_process, files_to_ignore = lod_read_directory(directory, time_pattern, file_patterns)
    processed = lod_process_directory(files_to_process, remove_mode, too_young_to_delete, max_files_to_store)
    console_output(processed, directory, remove, time_pattern, file_patterns, too_young_to_delete, max_files_to_store)

    if remove is True:
        if disable_log is False:
            write_log(processed, directory, time_pattern, file_patterns)
        for o in processed:
            if o["status"] in [types.FileStatus.OverMaxFiles, types.FileStatus.Delete]:
                if path.isfile(o["filename"]):
                    os_remove(o["filename"])
                elif path.isdir(o["filename"]):
                    rmtree(o["filename"])
    return processed, files_to_ignore


def main(arguments=None):
    """CLI entry point for TooManyFiles.

    Parses command-line arguments and executes directory scanning, simulation,
    listing, or file removal accordingly.

    Args:
        arguments (list[str], optional): List of command-line arguments (e.g., `['--pretend']`).
            If None, arguments are read from `sys.argv`. Defaults to None.
    """
    from .__init__ import __version__, __versiondate__

    parser = ArgumentParser(
        prog='toomanyfiles',
        description=_('Search date and time patterns to delete innecesary files or directories'),
        epilog=_("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year),
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('--version', action='version', version=__version__)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--remove', help=_("Removes files permanently"), action="store_true", default=False)
    group.add_argument('--pretend', help=_("Makes a simulation and doesn't remove files"), action="store_true", default=False)
    group.add_argument('--list', help=_("List files included and excluded"), action="store_true", default=False)

    modifiers = parser.add_argument_group(title=_("Modifiers to use with --remove and --pretend"), description=None)
    modifiers.add_argument('--time_pattern', help=_("Defines a python datetime pattern to search in current directory. The default pattern is '%(default)s'."), action="store", default="%Y%m%d %H%M")
    modifiers.add_argument('--file_patterns', help=_("Defines one or several string patterns to search in path with matches time pattern. Patterns are case sensitive and filename must have all to be selected. The default pattern is '%(default)s'."), action="append", default=[])
    modifiers.add_argument('--disable_log', help=_("Disable log generation. The default value is '%(default)s'."), action="store_true", default=False)
    modifiers.add_argument('--remove_mode', help=_("Remove mode. The default value is '%(default)s'."), choices=['RemainFirstInMonth', 'RemainLastInMonth'], default='RemainFirstInMonth')
    modifiers.add_argument('--too_young_to_delete', help=_("Number of days to respect from today. The default value is '%(default)s'."), default=30, type=int)
    modifiers.add_argument('--max_files_to_store', help=_("Maximum number of files to remain in directory. The default value is '%(default)s'."), default=100000000, type=int)

    args = parser.parse_args(arguments)

    init(autoreset=True)
    if args.remove:
        toomanyfiles(getcwd(), True, args.time_pattern, args.file_patterns, args.too_young_to_delete, args.max_files_to_store, types.RemoveMode.from_string(args.remove_mode), args.disable_log)
    if args.pretend:
        toomanyfiles(getcwd(), False, args.time_pattern, args.file_patterns, args.too_young_to_delete, args.max_files_to_store, types.RemoveMode.from_string(args.remove_mode), args.disable_log)
    if args.list:
        files_to_process, files_to_ignore = lod_read_directory(getcwd(), args.time_pattern, args.file_patterns)
        processed = lod_process_directory(files_to_process, types.RemoveMode.from_string(args.remove_mode), args.too_young_to_delete, args.max_files_to_store)

        processed = lod.lod_order_by(processed, "filename")
        files_to_ignore = lod.lod_order_by(files_to_ignore, "filename")

        print(colors.magenta("=== " + _("FILES TO PROCESS") + " ==="))
        print_with_type(processed)
        print()
        print(colors.magenta("=== " + _("FILES IGNORED") + " ==="))
        print_with_type(files_to_ignore)


def print_with_type(lod_):
    """Print formatted file details and status to the console for the --list command.

    Args:
        lod_ (list[dict]): List of file dictionaries to print.
    """
    for o in lod_:
        print(
            "  * ",
            colors.yellow(_("DIRECTORY")) if o["type"] == _("Directory") else colors.white(_("FILE")),
            path.basename(o["filename"]),
            colors.red(o["reason"]) if "reason" in o else "",
            _('Time pattern found: ({0})').format(o["dt"]) if "dt" in o else ""
        )


