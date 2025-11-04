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


