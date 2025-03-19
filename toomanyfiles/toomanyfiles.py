from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from gettext import translation
from importlib.resources import files
from os import getcwd, listdir, sep, path, remove, makedirs
from shutil import rmtree
from sys import exit
from toomanyfiles import types

try:
    t=translation('toomanyfiles', files("toomanyfiles/") / 'locale')
    _=t.gettext
except:
    _=str


class FilenameWithDatetime:
    def __init__(self, filename,datetime):
        self.filename=filename
        self.datetime=datetime
        self.status=types.FileStatus.Delete

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
    def __init__(self, directory,  time_pattern,  file_patterns):
        self.arr=[]
        self.__too_young_to_delete=30
        self.__max_files_to_store=100000000# Infinity
        self.__logging=True
        self.__remove_mode=types.RemoveMode.RemainFirstInMonth
        self.__pretending=1# Tag to set if we are using pretending or not. Can take None: Nor remove nor pretend, 0 Remove, 1 Pretend
        
        self.time_pattern=time_pattern
        self.file_patterns=file_patterns
        for filename in listdir(directory):
            filename= directory + sep + filename
            dt=datetime_in_filename(filename, time_pattern)
            if dt is not None:
                #Selects if matches all file_patterns
                found_file_patterns=True
                if len(self.file_patterns)>0:
                    for fp in self.file_patterns:
                        if not fp in filename:
                            found_file_patterns=False
                            break
                            
                if found_file_patterns:
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

    ## Number of files with date and time pattern detected
    def length(self):
        return len(self.arr)

    ## Changes the status of the FilenameWithDatetime objects in the array
    def __set_filename_status(self):
        aux=[]#Strings contining YYYYMM
        r=[]
        if self.remove_mode==types.RemoveMode.RemainFirstInMonth:
            self.__sort_by_datetime() ## From older to younger

            #Set status too_young
            if self.length()>=self.too_young_to_delete:
                for o in self.arr[self.length()-self.too_young_to_delete:self.length()]:
                    o.status=types.FileStatus.TooYoungToDelete
            else:
                for o in self.arr:
                    o.status=types.FileStatus.TooYoungToDelete

            #Leaving first in month
            if self.length()>=self.too_young_to_delete:
                for o in self.arr[0:self.length()-self.too_young_to_delete]:
                    if o.YYYYMM() not in aux:
                        o.status=types.FileStatus.Remain
                        r.append(o)
                        aux.append(o.YYYYMM())

            #r is a list of remaiun filename, so I can change status bigger to_store
            for i,o in enumerate(reversed(r)):
                if i>=self.max_files_to_store-self.too_young_to_delete:
                    o.status=types.FileStatus.OverMaxFiles

        elif self.remove_mode==types.RemoveMode.RemainLastInMonth:
            print(_("Not developed yet"))
            exit(types.ExitCodes.NotDeveloped)

    def __sort_by_datetime(self):
        self.arr=sorted(self.arr, key=lambda a: a.datetime  ,  reverse=False)

    #This function must be called after set status
    def __write_log(self, ):
        s=self.__header_string() + "\n"
        for o in self.arr:
            if o.status==types.FileStatus.Delete:
                 s=s+"{} >>> {}\n".format(o.filename, _("Delete"))
            elif o.status==types.FileStatus.OverMaxFiles:
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
        print(self.__header_string(color=True))
        if self.length()==0:
            return

        print (self.one_line_status())

        n_remain=self.__number_files_with_status(types.FileStatus.Remain)
        n_delete=self.__number_files_with_status(types.FileStatus.Delete)
        n_young=self.__number_files_with_status(types.FileStatus.TooYoungToDelete)
        n_over=self.__number_files_with_status(types.FileStatus.OverMaxFiles)
        if self.__pretending==1:
            print (_("Files status pretending:"))
            result=_("So, {} files will be deleted and {} will be kept when you use --remove parameter.").format(Fore.YELLOW + str(n_delete+n_over) + Style.RESET_ALL, Fore.YELLOW + str(n_remain+n_young) +Style.RESET_ALL)
        elif self.__pretending==0:
            print (_("File status removing:"))
            result=_("So, {} files have been deleted and {} files have been kept.").format(Fore.YELLOW + str(n_delete+n_over) + Style.RESET_ALL, Fore.YELLOW + str(n_remain+n_young) +Style.RESET_ALL)
        print ("  * {} [{}]: {}".format(_("Remains"), Fore.GREEN + _("R") + Style.RESET_ALL, n_remain))
        print ("  * {} [{}]: {}".format(_("Delete"), Fore.RED + _("D") + Style.RESET_ALL, n_delete))
        print ("  * {} [{}]: {}".format(_("Too young to delete"), Fore.MAGENTA + _("Y") + Style.RESET_ALL, n_young))
        print ("  * {} [{}]: {}".format(_("Over max files"), Fore.YELLOW + _("O") + Style.RESET_ALL, n_over))
        print(result)

    ## This mehod returns a colored string with the status of the files in the array in just one line
    ## @code
    ## PBBBBBPBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPBBBBBBBBBBBBBBBBBBBBBBBPBBBBBBBBBBBBBBBBBBBBJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ
    ## @endcode
    ## @return string
    def one_line_status(self):
        s=""
        for o in self.arr:
            if o.status==types.FileStatus.Remain:
                 s=s+"{}".format( Fore.GREEN + _("R") + Fore.RESET)
            elif o.status==types.FileStatus.Delete:
                 s=s+"{}".format( Fore.RED + _("D") + Fore.RESET)
            elif o.status==types.FileStatus.TooYoungToDelete:
                 s=s+"{}".format( Fore.MAGENTA + _("Y")+ Style.RESET_ALL)
            elif o.status==types.FileStatus.OverMaxFiles:
                 s=s+"{}".format( Fore.YELLOW + _("O")+ Style.RESET_ALL)
        return s

    ## Function that generates the header used in console output and in log
    ## @return string
    def __header_string(self,color=False):
        if color==True:
            return _("{} TooManyFiles in {} detected {} files with time pattern {} and filename patterns {}").format(Style.BRIGHT + str(datetime.now()) + Style.RESET_ALL,
                                                                                       Style.BRIGHT + Fore.YELLOW + getcwd() + Style.RESET_ALL,
                                                                                       Style.BRIGHT + Fore.GREEN + str(self.length()) + Style.RESET_ALL,
                                                                                       Fore.YELLOW + self.time_pattern + Style.RESET_ALL, 
                                                                                       Fore.YELLOW + str(self.file_patterns)+ Style.RESET_ALL, 
                                                                                       )
        else:
            return _("{} TooManyFiles in {} detected {} files with time pattern {} and filename patterns {}").format(datetime.now(), getcwd(), self.length(), self.time_pattern, str(self.file_patterns))


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
            if o.status in [types.FileStatus.OverMaxFiles, types.FileStatus.Delete]:
                if path.isfile(o.filename):
                    remove(o.filename)
                elif path.isdir(o.filename):
                    rmtree(o.filename)


## Function that retturn the length of the string
def len_pattern(pattern):
    return len(datetime.now().strftime(pattern))


## Finds the pattern in the filename and returns a datetime
def datetime_in_filename(filename,pattern):
    length=len_pattern(pattern)
    if len(filename)<len(pattern):
        return None
    for i in range(len(filename)-length+1):
        s=filename[i:length+i]
        try:
            return datetime.strptime(s,pattern)
        except:
            pass
    return None


def create_file(filename):        
    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename,"w"):
        pass

## Creates an example subdirectory and fills it with datetime pattern filenames
def create_examples():
    if path.exists('toomanyfiles_examples'):
        rmtree('toomanyfiles_examples')
    makedirs("toomanyfiles_examples/files", exist_ok=True)
    number=100
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/files/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
        create_file(filename)

    makedirs("toomanyfiles_examples/directories", exist_ok=True)
    number=100
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/directories/{}{:02d}{:02d} {:02d}{:02d} Directory/Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
        makedirs(path.dirname(filename), exist_ok=True)        
        create_file(filename)

    makedirs("toomanyfiles_examples/files_with_different_roots", exist_ok=True)
    number=5
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/files_with_different_roots/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example {}.txt".format(d.year,d.month,d.day,d.hour,d.minute, i)
        create_file(filename)

    print (Style.BRIGHT + _("Different examples have been created in the directory 'toomanyfiles_examples'"))

def remove_examples():
    if path.exists('toomanyfiles_examples'):
        rmtree('toomanyfiles_examples')
        print (_("'toomanyfiles_examples' directory removed"))
    else:
        print (_("I can't remove 'toomanyfiles_examples' directory"))


def toomanyfiles(directory,  remove, time_pattern="%Y%m%d %H%M", file_patterns=[],  too_young_to_delete=30, max_files_to_store=100000000, remove_mode="RemainFirstInMonth", disable_log=False):
    """
        Main function to call toomanyfiles programmatically
    
        @param remove Boolean. If True removes files that matches parameters. False only pretends
    """
    manager=FilenameWithDatetimeManager(directory, time_pattern,  file_patterns)
    
    manager.logging=not disable_log
    manager.remove_mode=types.RemoveMode.from_string(remove_mode)

    #Validations
    if manager.too_young_to_delete>manager.max_files_to_store:
        print(Fore.RED + _("The number of files too young to delete can't be bigger than the maximum number of files to store") + Style.RESET_ALL)
        exit(types.ExitCodes.YoungGTMax)

    if remove is True:
        manager.remove()
    else:
        manager.pretend()


## TooManyFiles main script
## If arguments is None, launches with argc parameters. Entry point is toomanyfiles:main
## You can call with main(['--pretend']). It's equivalento to system('toomanyfiles --pretend')
## @param arguments is an array with parser arguments. For example: ['--max_files_to_store','9']. 
def main(arguments=None):
    from .__init__ import __version__, __versiondate__
    
    parser=ArgumentParser(prog='toomanyfiles', description=_('Search date and time patterns to delete innecesary files or directories'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(__versiondate__.year)), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    group= parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create_examples', help=_("Create example directories"), action="store_true",default=False)
    group.add_argument('--remove_examples', help=_("Remove example directories'"), action="store_true",default=False)
    group.add_argument('--remove', help=_("Removes files permanently"), action="store_true", default=False)
    group.add_argument('--pretend', help=_("Makes a simulation and doesn't remove files"), action="store_true", default=False)

    modifiers=parser.add_argument_group(title=_("Modifiers to use with --remove and --pretend"), description=None)
    modifiers.add_argument('--time_pattern', help=_("Defines a python datetime pattern to search in current directory. The default pattern is '%(default)s'."), action="store",default="%Y%m%d %H%M")    
    modifiers.add_argument('--file_patterns', help=_("Defines one or several string patterns to search in path with matches time pattern. Patterns are case sensitive and filename must have all to be selected. The default pattern is '%(default)s'."), action="append", default=[])    
    modifiers.add_argument('--disable_log', help=_("Disable log generation. The default value is '%(default)s'."),action="store_true", default="")
    modifiers.add_argument('--remove_mode', help=_("Remove mode. The default value is '%(default)s'."), choices=['RemainFirstInMonth','RemainLastInMonth'], default='RemainFirstInMonth')
    modifiers.add_argument('--too_young_to_delete', help=_("Number of days to respect from today. The default value is '%(default)s'."), default=30, type=int)
    modifiers.add_argument('--max_files_to_store', help=_("Maximum number of files to remain in directory. The default value is '%(default)s'."), default=100000000, type=int)

    args=parser.parse_args(arguments)

    init(autoreset=True)
    
    

    if args.create_examples==True:
        create_examples()
        exit(types.ExitCodes.Success)
    if args.remove_examples==True:
        remove_examples()
        exit(types.ExitCodes.Success)


    if args.remove:
        remove=True
    if args.pretend:
        remove=False
    
    toomanyfiles(getcwd(), remove, args.time_pattern, args.file_patterns,   args.too_young_to_delete, args.max_files_to_store, args.remove_mode, args.disable_log)
