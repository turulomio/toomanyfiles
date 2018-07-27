#!/usr/bin/python3
import time
import colorama
import os
import subprocess

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

    def run(self):
        os.system("""xterm -hold -bg black -geometry 140x400  -fa monaco -fs 18 -fg white -e "ttyrec -e 'python3 demo.py'; ttygif ttyrecord" """)

if __name__ == "__main__":
    session=RecSession()
    
    session.comment("# This is a video to show how to use 'toomanyfiles' command")
    session.comment("# We are going to create an example directory to learn how to use it")
    session.command("toomanyfiles --create_example")
    session.run

