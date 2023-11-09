from datetime import date
from toomanyfiles import __version__
from os import system, chdir
from gettext import translation, install
from importlib.resources import files
from sys import modules
        
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
    chdir("doc/ttyrec")
    system("ttyrecgenerator --output toomanyfiles_howto_es 'python3 howto.py' --lc_all es_ES.UTF-8")
    system("ttyrecgenerator --output toomanyfiles_howto_en 'python3 howto.py' --lc_all C")
    chdir("../..")

def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o toomanyfiles/locale/toomanyfiles.pot toomanyfiles/*.py")
        system("msgmerge -N --no-wrap -U toomanyfiles/locale/es.po toomanyfiles/locale/toomanyfiles.pot")
        system("msgfmt -cv -o toomanyfiles/locale/es/LC_MESSAGES/toomanyfiles.mo toomanyfiles/locale/es.po")
       # system("msgfmt -cv -o toomanyfiles/locale/en/LC_MESSAGES/toomanyfiles.mo toomanyfiles/locale/en.po")

def man():
    for language in ('es', 'en'):
        mangenerator(language)

def mangenerator( language):
    """
        Create man pages for parameter language
    """
    from mangenerator import Man
    if language=="en":
        install('toomanyfiles', 'badlocale')
        man=Man("man/man1/toomanyfiles")
    else:
        lang1=translation('toomanyfiles', 'toomanyfiles/locale', languages=[language])
        lang1.install()
        man=Man("man/es/man1/toomanyfiles")
    print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

    man.setMetadata("toomanyfiles",  1,   date.today(), "Mariano Muñoz", _("Remove innecesary files or directories with a date and time pattern in the current directory."))
    man.setSynopsis("""[-h] [--version] (--create_example | --remove | --pretend)
                    [--pattern PATTERN] [--disable_log]
                    [--remove_mode {RemainFirstInMonth,RemainLastInMonth}]
                    [--too_young_to_delete TOO_YOUNG_TO_DELETE]
                    [--max_files_to_store MAX_FILES_TO_STORE]""")
    man.header(_("DESCRIPTION"), 1)
    man.paragraph(_("This app has the following mandatory parameters:"), 1)
    man.paragraph("--create_example", 2, True)
    man.paragraph(_("Create two directories called 'example' and 'example_directories' in the current working directory and fill it with example files with date and time patterns."), 3)
    man.paragraph("--pretend", 2, True)
    man.paragraph(_("Makes a simulation selecting which files will be deleted when --remove parameter is used."), 3)
    man.paragraph("--remove", 2, True)
    man.paragraph(_("Deletes files. Be careful, This can't be unmade. Use --pretend before."), 3)
    
    man.paragraph(_("With --pretend and --remove you can use this parameters:"), 1)
    man.paragraph("--pattern", 2, True)
    man.paragraph(_("Sets the date and time pattern to search in the current directory filenames. It uses python strftime function format."), 3)
    man.paragraph("--disable_log", 2, True)
    man.paragraph("--remove_mode", 2, True)
    man.paragraph("--too_young_to_delete", 2, True)
    man.paragraph("--max_files_to_store", 2, True)
    man.save()

def release():
    print(_("New Release:"))
    print(_("  * Change version and date in version.py"))
    print(_("  * Change version in pyproject.toml"))
    print(_("  * Edit Changelog in README.md"))
    print("  * poe translate")
    print("  * mcedit locale/es.po")
    print("  * poe translate")
    print("  * poe man")
    print("  * mcedit doc/ttyrec/howto.py")
    print("  * python setup.py video" + ". " + _("If changed restart from first python setup.py doc"))
    print("  * git commit -a -m 'toomanyfiles-{0}'".format(__version__))
    print("  * git push")
    print(_("  * Make a new tag in github"))
    print("  * poetry publish --username --password")
    print(_("  * Create a new gentoo ebuild with the new version"))
    print(_("  * Upload to portage repository")) 


