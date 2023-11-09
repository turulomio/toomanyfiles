from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from gettext import translation
from importlib.resources import files
from os import getcwd, listdir, sep, path, remove, makedirs
from shutil import rmtree
from sys import exit

try:
    t=translation('toomanyfiles', files("toomanyfiles/") / 'locale')
    _=t.gettext
except:
    _=str


class ExitCodes:
    Success=0
    MixedRoots=1
    MixedFilesDirectories=2
    NotDeveloped=3
    ArgumentError=4
    
    ##Younger files parameter bigger than max number of files
    YoungGTMax=5

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
        for filename in listdir(directory):
            filename= directory + sep + filename
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

    ## Number of files with date and time pattern detected
    def length(self):
        return len(self.arr)

    ## Changes the status of the FilenameWithDatetime objects in the array
    def __set_filename_status(self):
        # =========== SECURITY
        alldir=self.__all_filenames_are_directories()
        allfiles=self.__all_filenames_are_regular_files()
        roots=self.root_filenames()
        if len(roots)>1:
            print(_("I can't continue, there are different filename roots with date and time patterns:"))
            for root in roots:
                print ("  {} {}".format(Fore.GREEN + Style.BRIGHT + "*" + Style.RESET_ALL, root))
            exit(ExitCodes.MixedRoots)
            
        if alldir==False and allfiles==False:
            print(_("I can't continue, there are files and directories with date and time patterns in the current path"))
            exit(ExitCodes.MixedFilesDirectories)
        
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
            exit(ExitCodes.NotDeveloped)

    def __sort_by_datetime(self):
        self.arr=sorted(self.arr, key=lambda a: a.datetime  ,  reverse=False)
        
    ## Function that returns a list with the different filename roots in the currrenty directory
    def root_filenames(self):
        aux=[]
        for o in self. arr:
            root=o.filename_without_pattern(self.pattern)
            if root not in aux:
                aux.append(root)
        return aux

    #This function must be called after set status
    def __write_log(self, ):
        s=self.__header_string() + "\n"
        for o in self.arr:
            if o.status==FileStatus.Delete:
                 s=s+"{} >>> {}\n".format(o.filename, _("Delete"))
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

    ## Functions that detects if all FilenameWithDatetime are directories
    ## @return Bool
    def __all_filenames_are_directories(self):
        for o in self.arr:
            if path.isdir(o.filename)==False:
                return False
        return True
        
    ## Functions that detects if all FilenameWithDatetime are regular files
    ## @return Bool
    def __all_filenames_are_regular_files(self):
        for o in self.arr:
            if path.isfile(o.filename)==False:
                return False
        return True

    #This function must be called after set status
    def __console_output(self):
        print(self.__header_string(color=True))
        if self.length()==0:
            return

        print (self.one_line_status())

        n_remain=self.__number_files_with_status(FileStatus.Remain)
        n_delete=self.__number_files_with_status(FileStatus.Delete)
        n_young=self.__number_files_with_status(FileStatus.TooYoungToDelete)
        n_over=self.__number_files_with_status(FileStatus.OverMaxFiles)
        if self.__pretending==1:
            if self.__all_filenames_are_directories():
                print (_("Directories status pretending:"))
            elif self.__all_filenames_are_regular_files():
                print (_("File status pretending:"))
            result=_("So, {} files will be deleted and {} will be kept when you use --remove parameter.").format(Fore.YELLOW + str(n_delete+n_over) + Style.RESET_ALL, Fore.YELLOW + str(n_remain+n_young) +Style.RESET_ALL)
        elif self.__pretending==0:
            if self.__all_filenames_are_directories():
                print (_("Directories status removing:"))
            elif self.__all_filenames_are_regular_files():
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
            if o.status==FileStatus.Remain:
                 s=s+"{}".format( Fore.GREEN + _("R") + Fore.RESET)
            elif o.status==FileStatus.Delete:
                 s=s+"{}".format( Fore.RED + _("D") + Fore.RESET)
            elif o.status==FileStatus.TooYoungToDelete:
                 s=s+"{}".format( Fore.MAGENTA + _("Y")+ Style.RESET_ALL)
            elif o.status==FileStatus.OverMaxFiles:
                 s=s+"{}".format( Fore.YELLOW + _("O")+ Style.RESET_ALL)
        return s

    ## Function that generates the header used in console output and in log
    ## @return string
    def __header_string(self,color=False):
        if color==True:
            return _("{} TooManyFiles in {} detected {} files with pattern {}").format(Style.BRIGHT + str(datetime.now()) + Style.RESET_ALL,
                                                                                       Style.BRIGHT + Fore.YELLOW + getcwd() + Style.RESET_ALL,
                                                                                       Style.BRIGHT + Fore.GREEN + str(self.length()) + Style.RESET_ALL,
                                                                                       Fore.YELLOW + self.pattern + Style.RESET_ALL)
        else:
            return _("{} TooManyFiles in {} detected {} files with pattern {}").format(datetime.now(), getcwd(), self.length(), self.pattern)


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

## Creates an example subdirectory and fills it with datetime pattern filenames
def create_examples():
    makedirs("toomanyfiles_examples/files", exist_ok=True)
    number=1000
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/files/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
        f=open(filename,"w")
        f.close()

    makedirs("toomanyfiles_examples/directories", exist_ok=True)
    number=1000
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/directories/{}{:02d}{:02d} {:02d}{:02d} Directory/Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
        makedirs(path.dirname(filename), exist_ok=True)        
        f=open(filename,"w")
        f.close()

    makedirs("toomanyfiles_examples/files_with_different_roots", exist_ok=True)
    number=5
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/files_with_different_roots/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example {}.txt".format(d.year,d.month,d.day,d.hour,d.minute, i)
        f=open(filename,"w")
        f.close()


    print (Style.BRIGHT + _("Different examples have been created in the directory 'toomanyfiles_examples'"))

def remove_examples():
    if path.exists('toomanyfiles_examples'):
        rmtree('toomanyfiles_examples')
        print (_("'toomanyfiles_examples' directory removed"))
    else:
        print (_("I can't remove 'toomanyfiles_examples' directory"))


def toomanyfiles(remove, pattern="%Y%m%d %H%M", too_young_to_delete=30, max_files_to_store=100000000, remove_mode="RemainFirstInMonth", disable_log=False):
    """
        Main function to call toomanyfiles programmatically
    
        @param remove Boolean. If True removes files that matches parameters. False only pretends
    """
    manager=FilenameWithDatetimeManager(getcwd(), pattern)
    
    manager.logging=not disable_log
    manager.remove_mode=RemoveMode.from_string(remove_mode)

    #Validations
    if manager.too_young_to_delete>manager.max_files_to_store:
        print(Fore.RED + _("The number of files too young to delete can't be bigger than the maximum number of files to store") + Style.RESET_ALL)
        exit(ExitCodes.YoungGTMax)

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
    modifiers.add_argument('--pattern', help=_("Defines a python datetime pattern to search in current directory. The default pattern is '%(default)s'."), action="store",default="%Y%m%d %H%M")
    modifiers.add_argument('--disable_log', help=_("Disable log generation. The default value is '%(default)s'."),action="store_true", default=False)
    modifiers.add_argument('--remove_mode', help=_("Remove mode. The default value is '%(default)s'."), choices=['RemainFirstInMonth','RemainLastInMonth'], default='RemainFirstInMonth')
    modifiers.add_argument('--too_young_to_delete', help=_("Number of days to respect from today. The default value is '%(default)s'."), default=30, type=int)
    modifiers.add_argument('--max_files_to_store', help=_("Maximum number of files to remain in directory. The default value is '%(default)s'."), default=100000000, type=int)

    args=parser.parse_args(arguments)

    init(autoreset=True)
    
    

    if args.create_examples==True:
        create_examples()
        exit(ExitCodes.Success)
    if args.remove_examples==True:
        remove_examples()
        exit(ExitCodes.Success)


    if args.remove:
        remove=True
    if args.pretend:
        remove=False
    
    toomanyfiles(remove, args.pattern,  args.too_young_to_delete, args.max_files_to_store, args.remove_mode, args.disable_log)
