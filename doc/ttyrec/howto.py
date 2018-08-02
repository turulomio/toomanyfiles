#!/usr/bin/python3
import argparse
import time
import colorama
import os
import subprocess
import gettext
import sys
sys.path.append("/usr/lib/toomanyfiles")

from libttyrecgenerator import RecSession
# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work
gettext.install('toomanyfiles', '/usr/share/locale')

parser=argparse.ArgumentParser(description='HOWTO to save with ttyrec', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--language', help=_("Sets output language"), action="store",default='en')
args=parser.parse_args()

r=RecSession()
r.change_language(args.language)
r.comment("# " + _("This is a video to show how to use 'toomanyfiles' command"))
r.comment("# " + _("We are going to create an example directory to learn how to use it"))
r.command("toomanyfiles --create_example")

r.comment("# " + _("We are going to see the 10 last files of this directory"))
r.command_pipe("ls -la example","tail -n 10")

r.comment("# " + _("We can see files with temporal pattern 'YYYYmmdd HHMM' with a day variation"))
r.comment("# " + _("We use to find this kind of files in automatic backups, logs, ..."))
r.comment("# " + _("If we want to save our disk space and we want to keep some of them, we can use TooManyFiles program"))
print()
r.comment("# " + _("So, We want to keep the last 5 files because they are too recent."))
r.comment("# " + _("We want to keep the first file of each month from the rest of the files until a max number the files of 15."))
time.sleep(3)
print()
r.comment("# " + _("We enter in the example directory."))
r.chdir("example")

r.comment("# " + _("We make a simulation with --pretend"))
r.command("toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --pretend")
time.sleep(2)

r.comment("# " + _("We analyze the result with the output.."))
r.comment("# " + _("We like the result, so we can delete files replacing --pretend by --remove. Selected files will be removed permanently"))
r.command("toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --remove")
time.sleep(2)

r.comment("# " + _("We list the files remaining"))
r.command("ls -la")

os.system("rm -Rf ../example")
os.system("rm -Rf ../example_directories")
r.comment("# " + _("That's all"))
time.sleep(20)
sys.exit(0)