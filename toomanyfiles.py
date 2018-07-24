#!/usr/bin/python3
import argparse
import colorama
import datetime
import gettext
import os

# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work
gettext.textdomain('toomanyfiles')
_=gettext.gettext


class FilenameWithDatetime:
    def __init__(self, filename,datetime):
        self.filename=filename
        self.datetime=datetime
    
    def YYYYMM(self):
        return "{}{:02d}".format(self.datetime.year,self.datetime.month)
        
    def __repr__(self):
        return("FWD: {}".format(self.filename))


class FilenameWithDatetimeManager:
    def __init__(self):
        self.arr=[]

    def append(self,o):
        self.arr.append(o)

    def length(self):
        return len(self.arr)

    def print_datetime(self):
        for o in self.arr:
            print (o.filename, ">>>", o.datetime)

    def list_remain(self):
        aux=[]#Strings contining YYYYMM
        r=[]
        self.sort_by_datetime()
        for o in self.arr:
            if o.YYYYMM() not in aux:
                aux.append(o.YYYYMM())
                r.append(o)
        return r

    def sort_by_datetime(self):
        self.arr=sorted(self.arr, key=lambda a: a.datetime  ,  reverse=False)

    def pretend(self):
        remain=self.list_remain()
        for o in self.arr:
            if o in remain:
                 print(colorama.Fore.GREEN + str(o))
            else:
                 print(colorama.Fore.RED + str(o))

    def remove(self):
        remain=self.list_remain()
        for o in self.arr:
            if o not in remain:
                 os.remove(filename)


def makedirs(dir):
    try:
       os.mkdir(dir)
    except:
       pass

## Function that retturn the length of the string
def len_pattern(pattern):
    return len(datetime.datetime.now().strftime(pattern))


## Finds the pattern in the filename and returns a datetime
def datetime_in_filename(filename,pattern):
    length=len_pattern(pattern)
    if len(filename)<len(pattern):
        return None
    for i in range(len(filename)-length):
        s=filename[i:length+i]
        try:
            return datetime.datetime.strptime(s,pattern)
        except:
            pass
    return None




if __name__ == '__main__':
    parser=argparse.ArgumentParser(prog='Makefile.py', description=_('TooManyFiles Makefile'), epilog=_("Developed by Mariano Muñoz"), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--pattern', help="Definies a python datetime pattern", action="store",default="%Y%m%d %H%M")
    parser.add_argument('--create_example', help="Create a example of files", action="store_true",default=False)
    parser.add_argument('--remove', help="Removes files permanently",action="store_true", default=False)
    parser.add_argument('--mode', help="Remove mode.", choices=['RemainFirstInMonth','RemainLastInMonth'],default="RemainFirstInMonth")
    parser.add_argument('--respect', help="Number of days to respect",default=30)
    
    args=parser.parse_args()

    if args.create_example==True:
        makedirs("example")
        for i in range (1000):
            d=datetime.datetime.now()-datetime.timedelta(days=i)
            filename="example/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
            f=open(filename,"w")
            f.close()
        print (_("Created 1000 files in the directory 'example'"))
        sys.exit(0)


    manager=FilenameWithDatetimeManager()
    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            filename= subdir + os.sep + file
            dt=datetime_in_filename(filename,args.pattern)
            if dt!=None:
                manager.append(FilenameWithDatetime(filename,dt))

    manager.pretend()
    if args.remove==True:
         manager.remove()
