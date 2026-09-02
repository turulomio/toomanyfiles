"""TooManyFiles - Tool and library to remove obsolete files and directories.

Search date and time patterns in filenames to clean up unnecessary files or directories
while preserving specific retention policies (e.g., monthly backups, young files).
Provides CLI utilities and modules for single-directory, JSON configuration, and recursive tree cleanup.
"""

from toomanyfiles import toomanyfiles
from toomanyfiles import json
from toomanyfiles import tree

from datetime import datetime
__version__ = '1.3.0'
__versiondatetime__ = datetime(2026, 9, 2, 4, 34)
__versiondate__ = __versiondatetime__.date()

