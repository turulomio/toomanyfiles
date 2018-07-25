#!/usr/bin/python3
import argparse
import colorama
import datetime
import gettext
import os
import sys

version="20180724"

def version_date():
    versio=version.replace("+","")
    return datetime.date(int(versio[:-4]),  int(versio[4:-2]),  int(versio[6:]))

# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work. Nuevo sistema2
gettext.install('toomanyfiles')


class RemoveMode:
    RemainFirstInMonth=1
    RemainLastInMonth=2

class FilenameStatus:
    TooYoungToDelete=1
    OverMaxFiles=2
    Remain=3
    Delete=4


class FilenameWithDatetime:
    def __init__(self, filename,datetime):
        self.filename=filename
        self.datetime=datetime
        self.status=FilenameStatus.Delete

    def YYYYMM(self):
        return "{}{:02d}".format(self.datetime.year,self.datetime.month)
        
    def __repr__(self):
        return("FWD: {}".format(self.filename))

## Only extracts files in current directory
class FilenameWithDatetimeManager:
    def __init__(self, directory):
        self.arr=[]
        self.mode=RemoveMode.RemainFirstInMonth
        self.too_young_to_delete=30
        self.max_files_to_store=60
        self._log=False
        for filename in os.listdir(directory):
            filename= directory + os.sep + filename
            if os.path.isdir(filename)==False:
                dt=datetime_in_filename(filename,args.pattern)
                if dt!=None:
                    self.append(FilenameWithDatetime(filename,dt))
                    
    @property
    def log(self):
        return self._log
    @log.setter
    def log(self,value):
        self._log=value

    def append(self,o):
        self.arr.append(o)

    def length(self):
        return len(self.arr)

    def print_datetime(self):
        for o in self.arr:
            print (o.filename, ">>>", o.datetime)

    def set_status(self):
        aux=[]#Strings contining YYYYMM
        r=[]
        if self.mode==RemoveMode.RemainFirstInMonth:
            self.sort_by_datetime() ## From older to younger

            #Set status too_young
            if self.length()>=self.too_young_to_delete:
                for o in self.arr[self.length()-self.too_young_to_delete:self.length()]:
                    o.status=FilenameStatus.TooYoungToDelete
            else:
                for o in self.arr:
                    o.status=FilenameStatus.TooYoungToDelete

            #Leaving first in month
            if self.length()>=self.too_young_to_delete:
                for o in self.arr[0:self.length()-self.too_young_to_delete]:
                    if o.YYYYMM() not in aux:
                        o.status=FilenameStatus.Remain
                        r.append(o)
                        aux.append(o.YYYYMM())

            #r is a list of remaiun filename, so I can change status bigger to_store
            for i,o in enumerate(reversed(r)):
                if i>self.max_files_to_store-self.too_young_to_delete:
                    o.status=FilenameStatus.OverMaxFiles

    def sort_by_datetime(self):
        self.arr=sorted(self.arr, key=lambda a: a.datetime  ,  reverse=False)


    #This function must be called after set status
    def pretend(self):
        s="TooManyFiles was executed at {}\n".format(datetime.datetime.now())
        for o in self.arr:
            if o.status==FilenameStatus.Remain:
                 s=s+"{} >>> {}\n".format(o.filename, colorama.Fore.GREEN + _("Remains"))
            elif o.status==FilenameStatus.Delete:
                 s=s+"{} >>> {}\n".format(o.filename, colorama.Fore.RED + _("Delete"))
            elif o.status==FilenameStatus.TooYoungToDelete:
                 s=s+"{} >>> {}\n".format(o.filename, colorama.Fore.GREEN + colorama.Style.BRIGHT + _("Too young to delete"))
            elif o.status==FilenameStatus.OverMaxFiles:
                 s=s+"{} >>> {}\n".format(o.filename, colorama.Fore.RED + colorama.Style.BRIGHT + _("Over max number of files"))
        print (s)
        if self.log==True:
            f=open("TooManyFiles.log","a")
            f.write(s)
            f.close()




    def remove(self):
        for o in self.arr:
            if o.status in [FilenameStatus.OverMaxFiles, FilenameStatus.Delete]:
                 os.remove(o.filename)


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
    parser=argparse.ArgumentParser(prog='toomanyfiles', description=_('Seach datetime patterns to delete innecesary files'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(version_date().year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=version)
    parser.add_argument('--pattern', help=_("Defines a python datetime pattern to search in current directory"), action="store",default="%Y%m%d %H%M")
    parser.add_argument('--create_example', help=_("Create a example files in directory 'example'"), action="store_true",default=False)
    parser.add_argument('--remove', help=_("Removes files permanently. If not selected shows information"),action="store_true", default=False)
    parser.add_argument('--log', help=_("Appends information in currrent directory log"),action="store_true", default=False)
    parser.add_argument('--mode', help=_("Remove mode"), choices=['RemainFirstInMonth','RemainLastInMonth'], default='RemainFirstInMonth')
    parser.add_argument('--too_young_to_delete', help=_("Number of days to respect from today"), default=30)
    parser.add_argument('--max_files_to_store', help=_("Maximum number of files to remain in directory"), default=60)
    
    args=parser.parse_args()

    colorama.init(autoreset=True)

    if args.create_example==True:
        makedirs("example")
        for i in range (10000):
            d=datetime.datetime.now()-datetime.timedelta(days=i)
            filename="example/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
            f=open(filename,"w")
            f.close()
        print (_("Created 10000 files in the directory 'example'"))
        sys.exit(0)


    manager=FilenameWithDatetimeManager(os.getcwd())
    manager.too_young_to_delete=int(args.too_young_to_delete)
    manager.max_files_to_store=int(args.max_files_to_store)
    manager.log=True
    manager.set_status()
    manager.pretend()
    if args.remove==True:
         manager.remove()
