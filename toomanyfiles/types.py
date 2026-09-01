
"""Constants, exit codes, enumeration types, and status values used across TooManyFiles."""


class ExitCodes:
    """Process exit status codes returned by TooManyFiles CLI and operations."""

    Success = 0
    MixedRoots = 1
    MixedFilesDirectories = 2
    NotDeveloped = 3
    ArgumentError = 4

    # Younger files parameter bigger than max number of files
    YoungGTMax = 5


class RemoveMode:
    """Strategy modes for choosing which files to retain during cleanup."""

    RemainFirstInMonth = 1
    RemainLastInMonth = 2

    @staticmethod
    def from_string(s):
        """Convert a string representation of RemoveMode to its integer constant.

        Args:
            s (str): String identifier ("RemainFirstInMonth" or "RemainLastInMonth").

        Returns:
            int | None: Corresponding RemoveMode constant, or None if unrecognized.
        """
        if s == "RemainFirstInMonth":
            return RemoveMode.RemainFirstInMonth
        elif s == "RemainLastInMonth":
            return RemoveMode.RemainLastInMonth


class FileStatus:
    """Processing and retention status flags assigned to individual files."""

    TooYoungToDelete = 1
    OverMaxFiles = 2
    Remain = 3
    Delete = 4


