#!/usr/bin/python3
import argparse
import datetime
import gettext
import os

# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work
gettext.textdomain('toomanyfiles')
_=gettext.gettext

def makedirs(dir):
    try:
       os.mkdir(dir)
    except:
       pass


if __name__ == '__main__':
    parser=argparse.ArgumentParser(prog='Makefile.py', description=_('TooManyFiles Makefile'), epilog=_("Developed by Mariano Muñoz"), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--pattern', help="Create a example of files", action="store_true",default=False)
    parser.add_argument('--create_example', help="Create a example of files", action="store_true",default=False)
    parser.add_argument('--write', help="Removes files permanently",action="store_true", default=False)
    args=parser.parse_args()

    if args.create_example==True:
        makedirs("example")
        for i in range (1000):
            d=datetime.datetime.now()-datetime.timedelta(days=i)
            filename="example/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
            f=open(filename,"w")
            f.close()
        print (_("Created 1000 files in the directory 'example'"))
