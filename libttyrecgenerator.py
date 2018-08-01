#!/usr/bin/python3
import argparse
import time
import colorama
import datetime
import gettext
import os
import subprocess
#from toomanyfiles import version, version_date


version="20180727"

def version_date():
    versio=version.replace("+","")
    return datetime.date(int(versio[:-4]),  int(versio[4:-2]),  int(versio[6:]))




# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work. Nuevo sistema2
gettext.install('toomanyfiles')

class RecSession:
    def __init__(self):
        self.__hostname="MyLinux"
        self.__cwd="/home/ttyrec/"
        
    def path(self):
        return "{} {}".format(colorama.Fore.RED + "sg" + colorama.Style.RESET_ALL, colorama.Fore.BLUE + "/ttyrec/ # " + colorama.Style.RESET_ALL)

    ## # must be added to s
    def comment(self, s, sleep=4):
        print(self.path()+ colorama.Fore.YELLOW + s + colorama.Style.RESET_ALL)
        time.sleep(sleep)

    def command(self, s, sleep=6):
        print()
        print(self.path() + colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)
        print(subprocess.check_output(s,shell=True).decode('utf-8'))
        time.sleep(sleep)

    def chdir(self, dir, sleep=6):
        print()
        print(self.path() + colorama.Fore.GREEN + "cd " + dir + colorama.Style.RESET_ALL)
        os.chdir(dir)
        print()
        time.sleep(sleep)


    def command_pipe(self, c1,c2, sleep=6):
        cmd = "{}|{}".format(c1,c2)
        print()
        print(self.path() + colorama.Fore.GREEN + cmd + colorama.Style.RESET_ALL)
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0]
        print (output.decode('utf-8'))
        time.sleep(6)


