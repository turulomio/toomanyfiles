from datetime import date
from toomanyfiles import __version__, toomanyfiles
from os import system, chdir, path, makedirs
from shutil import rmtree, which
from datetime import datetime, timedelta
from colorama import Style
from gettext import translation
from importlib.resources import files
from sys import modules, exit
        
try:
    t=translation('toomanyfiles', files("toomanyfiles") / 'locale')
    _=t.gettext
except:
    _=str


def module_content():
    print(dir(modules["toomanyfiles"]))

def pytest():
    system("pytest")
    
def coverage():
    system("coverage run --omit='*/reusing/*,*uno.py' -m pytest && coverage report && coverage html")


def video():
    # Comprobaciones
    vhs=which("vhs")
    if vhs is None: 
        print(_("vhs tool is needed. Look at https://github.com/charmbracelet/vhs"))
        exit(1)

    create_examples()
    chdir("toomanyfiles_examples")
    #remove_examples()
    chdir("..")


def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o toomanyfiles/locale/toomanyfiles.pot toomanyfiles/*.py")
        system("msgmerge -N --no-wrap -U toomanyfiles/locale/es.po toomanyfiles/locale/toomanyfiles.pot")
        system("msgfmt -cv -o toomanyfiles/locale/es/LC_MESSAGES/toomanyfiles.mo toomanyfiles/locale/es.po")
       # system("msgfmt -cv -o toomanyfiles/locale/en/LC_MESSAGES/toomanyfiles.mo toomanyfiles/locale/en.po")


def release():
    print(_("New Release:"))
    print(_("  * Change version and date in __init__.py"))
    print(_("  * Change version in pyproject.toml"))
    print(_("  * Edit Changelog in README.md"))
    print("  * poe translate")
    print("  * mcedit locale/es.po")
    print("  * poe translate")
    print("  * mcedit doc/ttyrec/howto.py")
    print("  * python setup.py video" + ". " + _("If changed restart from first python setup.py doc"))
    print("  * git commit -a -m 'toomanyfiles-{0}'".format(__version__))
    print("  * git push")
    print(_("  * Make a new tag in github"))
    print("  * poetry publish --username --password")
    print(_("  * Create a new gentoo ebuild with the new version"))
    print(_("  * Upload to portage repository")) 


## Creates an example subdirectory and fills it with datetime pattern filenames
def create_examples():
    if path.exists('toomanyfiles_examples'):
        rmtree('toomanyfiles_examples')
    makedirs("toomanyfiles_examples/files", exist_ok=True)
    number=100
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/files/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
        toomanyfiles.create_file(filename)

    makedirs("toomanyfiles_examples/directories", exist_ok=True)
    number=100
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/directories/{}{:02d}{:02d} {:02d}{:02d} Directory/Toomanyfiles example.txt".format(d.year,d.month,d.day,d.hour,d.minute)
        makedirs(path.dirname(filename), exist_ok=True)        
        toomanyfiles.create_file(filename)

    makedirs("toomanyfiles_examples/files_with_different_roots", exist_ok=True)
    number=5
    for i in range (number):
        d=datetime.now()-timedelta(days=i)
        filename="toomanyfiles_examples/files_with_different_roots/{}{:02d}{:02d} {:02d}{:02d} Toomanyfiles example {}.txt".format(d.year,d.month,d.day,d.hour,d.minute, i)
        toomanyfiles.create_file(filename)

    print (Style.BRIGHT + _("Different examples have been created in the directory 'toomanyfiles_examples'"))

def remove_examples():
    if path.exists('toomanyfiles_examples'):
        rmtree('toomanyfiles_examples')
        print (_("'toomanyfiles_examples' directory removed"))
    else:
        print (_("I can't remove 'toomanyfiles_examples' directory"))