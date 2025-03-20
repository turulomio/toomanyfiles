from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from gettext import translation
from importlib.resources import files
from os import getcwd, listdir, sep, path, remove as os_remove, makedirs
from pydicts import lod
from shutil import rmtree
from sys import exit
from toomanyfiles import types

try:
    t=translation('toomanyfiles', files("toomanyfiles/") / 'locale')
    _=t.gettext
except:
    _=str

def datetime_in_filename(filename,pattern):
    """
        Finds the pattern in the basename of the filename and returns a datetime iterating alll characters
    """
    length=len(datetime.now().strftime(pattern))#Len of the value of the pattern

    basename=path.basename(filename)
    if len(basename)<len(pattern):
        return None
    for i in range(len(basename)-length+1):
        s=filename[i:length+i]
        try:
            dt=datetime.strptime(s,pattern)
            return dt
        except:
            pass
    return None

def header_string(lod_, directory,  time_pattern,  file_patterns, color=False):
    if color==True:
        return _("{} TooManyFiles in {} detected {} files with time pattern {} and filename patterns {}").format(Style.BRIGHT + str(datetime.now()) + Style.RESET_ALL,
                                                                                   Style.BRIGHT + Fore.YELLOW + directory + Style.RESET_ALL,
                                                                                   Style.BRIGHT + Fore.GREEN + str(len(lod_)) + Style.RESET_ALL,
                                                                                   Fore.YELLOW + time_pattern + Style.RESET_ALL, 
                                                                                   Fore.YELLOW + str(file_patterns)+ Style.RESET_ALL, 
                                                                                   )
    else:
        return _("{} TooManyFiles in {} detected {} files with time pattern {} and filename patterns {}").format(datetime.now(), directory, len(lod_), time_pattern, str(file_patterns))

def console_output(lod_, directory,  remove,  time_pattern,  file_patterns, too_young_to_delete, max_files_to_store):
    ## Function that generates the header used in console output and in log
    ## @return string

    ## This mehod returns a colored string with the status of the files in the array in just one line
    ## @code
    ## PBBBBBPBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBPBBBBBBBBBBBBBBBBBBBBBBBPBBBBBBBBBBBBBBBBBBBBJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ
    ## @endcode
    ## @return string
    def one_line_status():
        s=""
        for o in lod_:
            if o["status"]==types.FileStatus.Remain:
                 s=s+"{}".format( Fore.GREEN + _("R") + Fore.RESET)
            elif o["status"]==types.FileStatus.Delete:
                 s=s+"{}".format( Fore.RED + _("D") + Fore.RESET)
            elif o["status"]==types.FileStatus.TooYoungToDelete:
                 s=s+"{}".format( Fore.MAGENTA + _("Y")+ Style.RESET_ALL)
            elif o["status"]==types.FileStatus.OverMaxFiles:
                 s=s+"{}".format( Fore.YELLOW + _("O")+ Style.RESET_ALL)
        return s
    
    print(header_string(lod_, directory,  time_pattern, file_patterns,  color=True))
    if len(lod_)==0:
        return
    print("   Parameters: Too yound to delete:",  too_young_to_delete,  "Max files to store",  max_files_to_store)


    print (one_line_status())

    n_remain=lod.lod_count(lod_,lambda d, index: d["status"]==types.FileStatus.Remain)
    n_delete=lod.lod_count(lod_,lambda d, index: d["status"]==types.FileStatus.Delete)
    n_young=lod.lod_count(lod_,lambda d, index: d["status"]==types.FileStatus.TooYoungToDelete)
    n_over=lod.lod_count(lod_,lambda d, index: d["status"]==types.FileStatus.OverMaxFiles)
    if remove is False:
        print (_("Files status pretending:"))
        result=_("So, {} files will be deleted and {} will be kept when you use --remove parameter.").format(Fore.YELLOW + str(n_delete+n_over) + Style.RESET_ALL, Fore.YELLOW + str(n_remain+n_young) +Style.RESET_ALL)
    else:
        print (_("File status removing:"))
        result=_("So, {} files have been deleted and {} files have been kept.").format(Fore.YELLOW + str(n_delete+n_over) + Style.RESET_ALL, Fore.YELLOW + str(n_remain+n_young) +Style.RESET_ALL)
    print ("  * {} [{}]: {}".format(_("Remains"), Fore.GREEN + _("R") + Style.RESET_ALL, n_remain))
    print ("  * {} [{}]: {}".format(_("Delete"), Fore.RED + _("D") + Style.RESET_ALL, n_delete))
    print ("  * {} [{}]: {}".format(_("Too young to delete"), Fore.MAGENTA + _("Y") + Style.RESET_ALL, n_young))
    print ("  * {} [{}]: {}".format(_("Over max files"), Fore.YELLOW + _("O") + Style.RESET_ALL, n_over))
    print(result)

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

def lod_read_directory(directory, time_pattern, file_patterns):
    r=[]
    for filename in listdir(directory):
        filename= directory + sep + filename
        dt=datetime_in_filename(filename, time_pattern)
        if dt is not None:
            #Selects if matches all file_patterns
            found_file_patterns=True
            for fp in file_patterns:
                if not fp in filename:
                    found_file_patterns=False
                    break
                        
            if found_file_patterns:
                r.append({
                    "filename":filename, 
                    "dt":dt, 
                    "status":None, 
                })
                
    lod.lod_order_by(r, "dt")
    return r
    
def lod_process_directory(lod_,  remove_mode,  too_young_to_delete,  max_files_to_store):
            
    # Process lod
    aux=[]#Strings contining YYYYMM
    if remove_mode==types.RemoveMode.RemainFirstInMonth:
        #Set status too_young
        if len(lod_)>=too_young_to_delete:
            for o in lod_[len(lod_)-too_young_to_delete:len(lod_)]:
                o["status"]=types.FileStatus.TooYoungToDelete
        else:
            for o in lod_:
                o["status"]=types.FileStatus.TooYoungToDelete

        #Leaving first in month
        if len(lod_)>=too_young_to_delete:
            for o in lod_[0:len(lod_)-too_young_to_delete]:
                tuple_ym=(o["dt"].year, o["dt"].month)
                if tuple_ym not in aux:
                    o["status"]=types.FileStatus.Remain
                    aux.append(tuple_ym)
                else:
                    o["status"]=types.FileStatus.Delete

        #r is a list of remaiun filename, so I can change status bigger to_store
        for i,o in enumerate(reversed(lod_)):
            if i>=max_files_to_store-too_young_to_delete:
                o["status"]=types.FileStatus.OverMaxFiles

    elif remove_mode==types.RemoveMode.RemainLastInMonth:
        print(_("Not developed yet"))
        exit(types.ExitCodes.NotDeveloped)

    return lod_
    
#This function must be called after set status
def write_log(lod_, directory,  time_pattern, file_patterns):
    s=header_string(lod_, directory,  time_pattern, file_patterns, color=False) + "\n"
    for o in lod_:
        if o["status"]==types.FileStatus.Delete:
             s=s+"{} >>> {}\n".format(o["filename"], _("Delete"))
        elif o["status"]==types.FileStatus.OverMaxFiles:
             s=s+"{} >>> {}\n".format(o["filename"], _("Over max number of files"))
    with open("TooManyFiles.log","a") as f:
        f.write(s)

def toomanyfiles(directory,  remove, time_pattern="%Y%m%d %H%M", file_patterns=[],  too_young_to_delete=30, max_files_to_store=100000000, remove_mode=types.RemoveMode.RemainFirstInMonth, disable_log=False):
    """
        Main function to call toomanyfiles programmatically
    
        @param remove Boolean. If True removes files that matches parameters. False only pretends
        
        @return list of dictionaries
    """
    if too_young_to_delete>max_files_to_store:
        print(Fore.RED + _("The number of files too young to delete can't be bigger than the maximum number of files to store") + Style.RESET_ALL)
        exit(types.ExitCodes.YoungGTMax)
    
    lodfiles=lod_read_directory(directory,  time_pattern,  file_patterns)
    lodfiles=lod_process_directory(lodfiles,  remove_mode,  too_young_to_delete,  max_files_to_store)
    console_output(lodfiles, directory, remove, time_pattern, file_patterns, too_young_to_delete, max_files_to_store)
    
    if remove is True:
        if disable_log is False:
            write_log(lodfiles, directory,  time_pattern,  file_patterns)
        for o in lodfiles:
            if o["status"] in [types.FileStatus.OverMaxFiles, types.FileStatus.Delete]:
                if path.isfile(o["filename"]):
                    os_remove(o["filename"])
                elif path.isdir(o["filename"]):
                    rmtree(o["filename"])
    print(lodfiles)
    return lodfiles

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
        toomanyfiles(getcwd(), True, args.time_pattern, args.file_patterns,   args.too_young_to_delete, args.max_files_to_store, types.RemoveMode.from_string(args.remove_mode), args.disable_log)
    if args.pretend:    
        toomanyfiles(getcwd(), False, args.time_pattern, args.file_patterns,   args.too_young_to_delete, args.max_files_to_store, types.RemoveMode.from_string(args.remove_mode), args.disable_log)

        
    
