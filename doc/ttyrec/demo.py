#!/usr/bin/python3
import time
import colorama
import os
import subprocess

def path():
    return "{} {}".format(colorama.Fore.RED + "sg" + colorama.Style.RESET_ALL, colorama.Fore.BLUE + "/ttyrec/ # " + colorama.Style.RESET_ALL)

## # must be added to s
def comment(s):
    print(path()+ colorama.Fore.YELLOW + s + colorama.Style.RESET_ALL)
    time.sleep(4)

def command(s):
    print()
    print(path() + colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)
    print(subprocess.check_output(s,shell=True).decode('utf-8'))
    time.sleep(6)

def chdir(dir):
    print()
    print(path() + colorama.Fore.GREEN + "cd " + dir + colorama.Style.RESET_ALL)
    os.chdir(dir)
    print()
    time.sleep(6)


def command_pipe(c1,c2):
    cmd = "{}|{}".format(c1,c2)
    print()
    print(path() + colorama.Fore.GREEN + cmd + colorama.Style.RESET_ALL)
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    print (output.decode('utf-8'))
    time.sleep(6)

comment("# This is a video to show how to use 'toomanyfiles' command")
comment("# We are going to create an example directory to learn how to use it")
command("toomanyfiles --create_example")

comment("# We are going to see the 10 last files of this directory")
command_pipe("ls -la example","tail -n 10")

comment("# We can see files with temporal pattern 'YYYYmmdd HHMM' with a day variation")
comment("# We use to find this kind of files in automatic backups, logs, ...")
comment("# If we want to save our disk space and we want to keep some of them, we can use TooManyFiles program")
print()
comment("# So, We want to keep the last 5 files because they are too recent.")
comment("# We want to keep the first file of each month from the rest of the files until a max number the files of 15.")
time.sleep(3)
print()
comment("# We enter in the example directory.")
chdir("example")

comment("# We make a simulation with --pretend")
command("toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --pretend")
time.sleep(2)

comment("# We analyze the result with the output..")
comment("# We like the result, so we can delete files replacing --pretend by --remove. Selected files will be removed permanently")
command("toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --remove")
time.sleep(2)

comment("# We list the files remaining")
command("ls -la")

os.system("rm -Rf ../example")
comment("# That's all")
time.sleep(20)