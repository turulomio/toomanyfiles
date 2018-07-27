#!/usr/bin/python3
import argparse
import colorama
import datetime
import gettext
import os
import sys

version="20180727"

def version_date():
    versio=version.replace("+","")
    return datetime.date(int(versio[:-4]),  int(versio[4:-2]),  int(versio[6:]))

# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work. Nuevo sistema2
gettext.install('toomanyfiles')

class RemoveMode:
    RemainFirstInMonth=1
    RemainLastInMonth=2

    @staticmethod
    def from_string(s):
        if s=="RemainFirstInMonth":
            return RemoveMode.RemainFirstInMonth
        elif s=="RemainLastInMonth":
            return RemoveMode.RemainLastInMonth

class FileStatus:
    TooYoungToDelete=1
    OverMaxFiles=2
    Remain=3
    Delete=4


class FilenameWithDatetime:
    def __init__(self, filename,datetime):
        self.filename=filename
        self.datetime=datetime
        self.status=FileStatus.Delete

    def YYYYMM(self):
        return "{}{:02d}".format(self.datetime.year,self.datetime.month)
        
    def __repr__(self):
        return("FWD: {}".format(self.filename))

    ## Function that returns the filename without pattern
    def filename_without_pattern(self, pattern):
        dt=datetime_in_filename(self.filename, pattern)
        if dt!=None:
            return  self.filename.replace(dt.strftime(pattern), "")
        return None

## Only extracts files in current directory
## This object has two itineraries 
## 1. Pretend. Show information in console
## 2. Write. Show information in console. Writes log. Delete innecesary files.
class FilenameWithDatetimeManager:
    def __init__(self, directory,  pattern):
        self.arr=[]
        self.__too_young_to_delete=30
        self.__max_files_to_store=100000000# Infinity
        self.__logging=True
        self.__remove_mode=RemoveMode.RemainFirstInMonth
        self.__pretending=1# Tag to set if we are using pretending or not. Can take None: Nor remove nor pretend, 0 Remove, 1 Pretend
        
        self.pattern=pattern
        for filename in os.listdir(directory):
            filename= directory + os.sep + filename
            if os.path.isdir(filename)==False:
                dt=datetime_in_filename(filename,pattern)
                if dt!=None:
                    self.append(FilenameWithDatetime(filename,dt))

    ## Property that returns if log must be done when remove is selected
    ## @return Int
    @property
    def logging(self):
        return self.__logging

    @logging.setter
    def logging(self,value):
        self.__logging=value

    ## Property that returns the value of the RemoveMode selected
    ## @return RemoveMode
    @property
    def remove_mode(self):
        return self.__remove_mode

    @remove_mode.setter
    def remove_mode(self,value):
        self.__remove_mode=value

    ## Property that returns the number of more modern files that are not going to be deleted
    @property
    def too_young_to_delete(self):
        return self.__too_young_to_delete
        
    ## Property that sets the number of more modern files that are not going to be deleted
    ## @param value Integer
    @too_young_to_delete.setter
    def too_young_to_delete(self, value):
        self.__too_young_to_delete=value

    ## Property that returns the max number of selected files  that are going to be remained. 
    ## @return Int
    @property
    def max_files_to_store(self):
        return self.__max_files_to_store
        
    ## Property that sets the max number of selected files  that are going to be remained. 
    ## @return Int
    @max_files_to_store.setter
    def max_files_to_store(self, value):
        self.__max_files_to_store=value

    def append(self,o):
        self.arr.append(o)

    def length(self):
        return len(self.arr)

    ## Changes the status of the FilenameWithDatetime objects in the array
    def __set_filename_status(self):
        # =========== SECURITY
        if self.__several_root_filenames()==True:
            print(_("There are files with datetime patterns with different roots"))
            print(_("Exiting..."))
            sys.exit(3)        
        
        #========== CODE
        aux=[]#Strings contining YYYYMM
        r=[]
        if self.remove_mode==RemoveMode.RemainFirstInMonth:
            self.__sort_by_datetime() ## From older to younger

            #Set status too_young
            if self.length()>=self.too_young_to_delete:
                for o in self.arr[self.length()-self.too_young_to_delete:self.length()]:
                    o.status=FileStatus.TooYoungToDelete
            else:
                for o in self.arr:
                    o.status=FileStatus.TooYoungToDelete

            #Leaving first in month
            if self.length()>=self.too_young_to_delete:
                for o in self.arr[0:self.length()-self.too_young_to_delete]:
                    if o.YYYYMM() not in aux:
                        o.status=FileStatus.Remain
                        r.append(o)
                        aux.append(o.YYYYMM())

            #r is a list of remaiun filename, so I can change status bigger to_store
            for i,o in enumerate(reversed(r)):
                if i>=self.max_files_to_store-self.too_young_to_delete:
                    o.status=FileStatus.OverMaxFiles

        elif self.remove_mode==RemoveMode.RemainLastInMonth:
            print(_("Not developed yet"))
            sys.exit(2)

    def __sort_by_datetime(self):
        self.arr=sorted(self.arr, key=lambda a: a.datetime  ,  reverse=False)
        
    ## Function that returns a boolean if there are differente filenames withourt pattern in the array
    def __several_root_filenames(self):
        aux=[]
        for o in self. arr:
            root=o.filename_without_pattern(self.pattern)
            if root not in aux:
                aux.append(root)
        if len(aux)>1:
            return True
        return False

    #This function must be called after set status
    def __write_log(self):
        s=self.__header_string() + "\n"
        for o in self.arr:
            if o.status==FileStatus.Remain:
                 s=s+"{} >>> {}\n".format(o.filename,  _("Remains"))
            elif o.status==FileStatus.Delete:
                 s=s+"{} >>> {}\n".format(o.filename, _("Delete"))
            elif o.status==FileStatus.TooYoungToDelete:
                 s=s+"{} >>> {}\n".format(o.filename, _("Too young to delete"))
            elif o.status==FileStatus.OverMaxFiles:
                 s=s+"{} >>> {}\n".format(o.filename, _("Over max number of files"))
        f=open("TooManyFiles.log","a")
        f.write(s)
        f.close()

    ## Returns the number of files in self.arr with the status passed as parameter
    def __number_files_with_status(self, filestatus):
        r=0
        for o in self.arr:
            if o.status==filestatus:
                r=r+1
        return r

    #This function must be called after set status
    def __console_output(self):
        s=self.__header_string() +"\n"
        for o in self.arr:
            if o.status==FileStatus.Remain:
                 s=s+"{}".format( colorama.Fore.GREEN + _("R") + colorama.Fore.RESET)
            elif o.status==FileStatus.Delete:
                 s=s+"{}".format( colorama.Fore.RED + _("D") + colorama.Fore.RESET)
            elif o.status==FileStatus.TooYoungToDelete:
                 s=s+"{}".format( colorama.Fore.MAGENTA + _("Y")+ colorama.Style.RESET_ALL)
            elif o.status==FileStatus.OverMaxFiles:
                 s=s+"{}".format( colorama.Fore.YELLOW + _("O")+ colorama.Style.RESET_ALL)
        print (s)
        
        n_remain=self.__number_files_with_status(FileStatus.Remain)
        n_delete=self.__number_files_with_status(FileStatus.Delete)
        n_young=self.__number_files_with_status(FileStatus.TooYoungToDelete)
        n_over=self.__number_files_with_status(FileStatus.OverMaxFiles)
        if self.__pretending==1:
            print (_("File status pretending:"))
            result=_("So, {} files will be deleted and {} will be kept when you use --remove parameter.".format(colorama.Fore.YELLOW + str(n_delete+n_over) + colorama.Style.RESET_ALL, colorama.Fore.YELLOW + str(n_remain+n_young) +colorama.Style.RESET_ALL))
        elif self.__pretending==0:
            print (_("File status removing:"))
            result=_("So, {} files have been deleted and {} files have been kept.".format(colorama.Fore.YELLOW + str(n_delete+n_over) + colorama.Style.RESET_ALL, colorama.Fore.YELLOW + str(n_remain+n_young) +colorama.Style.RESET_ALL))
        print ("  * {} [{}]: {}".format(_("Remains"), colorama.Fore.GREEN + _("R") + colorama.Style.RESET_ALL, n_remain))
        print ("  * {} [{}]: {}".format(_("Delete"), colorama.Fore.RED + _("D") + colorama.Style.RESET_ALL, n_delete))
        print ("  * {} [{}]: {}".format(_("Too young to delete"), colorama.Fore.MAGENTA + _("Y") + colorama.Style.RESET_ALL, n_young))
        print ("  * {} [{}]: {}".format(_("Over max files"), colorama.Fore.YELLOW + _("O") + colorama.Style.RESET_ALL, n_over))
        print(result)


    ## Function that generates the header used in console output and in log
    ## @return string
    def __header_string(self):
        return _("TooManyFiles was executed at {}".format(datetime.datetime.now()))


    ## Shows information in console
    def pretend(self):
        self.__pretending=1
        self.__set_filename_status()
        self.__console_output()

    ## Shows information in console
    ## Write log
    ## Delete Files
    def remove(self):
        self.__pretending=0
        self.__set_filename_status()
        self.__console_output()
        if self.logging==True:
            self.__write_log()
        for o in self.arr:
            if o.status in [FileStatus.OverMaxFiles, FileStatus.Delete]:
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

## Creates an example subdirectory and fills it with datetime pattern filenames
def create_example():
    makedirs("example")
    number=1000
    for i in range (number):
        d=datetime.datetime.now()-datetime.timedelta(days=i)
        filename="example/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
        f=open(filename,"w")
        f.close()
    print (_("Created {} files in the directory 'example'".format(number)))


parser=argparse.ArgumentParser(prog='toomanyfiles', description=_('Seach datetime patterns to delete innecesary files'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(version_date().year)), formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--version', action='version', version=version)

group= parser.add_mutually_exclusive_group(required=True)
group.add_argument('--create_example', help=_("Create a example files in directory 'example'"), action="store_true",default=False)
group.add_argument('--remove', help=_("Removes files permanently"),action="store_true", default=False)
group.add_argument('--pretend', help=_("Makes a simulation and doesn't remove files"),action="store_true", default=False)

modifiers=parser.add_argument_group(title=_("Modifiers to use with --remove and --pretend"), description=None)
modifiers.add_argument('--pattern', help=_("Defines a python datetime pattern to search in current directory. The default pattern is '%(default)s'."), action="store",default="%Y%m%d %H%M")
modifiers.add_argument('--disable_log', help=_("Disable log generation. The default value is '%(default)s'."),action="store_true", default=False)
modifiers.add_argument('--remove_mode', help=_("Remove mode. The default value is '%(default)s'."), choices=['RemainFirstInMonth','RemainLastInMonth'], default='RemainFirstInMonth')
modifiers.add_argument('--too_young_to_delete', help=_("Number of days to respect from today. The default value is '%(default)s'."), default=30)
modifiers.add_argument('--max_files_to_store', help=_("Maximum number of files to remain in directory. The default value is '%(default)s'."), default=100000000)
if __name__ == '__main__':
    args=parser.parse_args()

    colorama.init(autoreset=True)

    if args.create_example==True:
        create_example()
        sys.exit(0)

    manager=FilenameWithDatetimeManager(os.getcwd(), args.pattern)
    #setting properties to manager
    try:
        manager.too_young_to_delete=int(args.too_young_to_delete)
        manager.max_files_to_store=int(args.max_files_to_store)
        manager.logging=not args.disable_log
        manager.remove_mode=RemoveMode.from_string(args.remove_mode)
    except:
        print(_("Error passing parameters"))
        parser.print_help()
        sys.exit(1)

    #Validations
    if manager.too_young_to_delete>manager.max_files_to_store:
        print(colorama.Fore.RED + _("The number of files too young to delete can't be bigger than the maximum number of files to store") + colorama.Style.RESET_ALL)
        sys.exit(54)

    if args.remove==True:
        manager.remove()

    if args.pretend==True:
        manager.pretend()
