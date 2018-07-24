#!/usr/bin/python3
import argparse
import datetime
import os
import sys
from subprocess import call
from colorama import Style, Fore
from multiprocessing import cpu_count
from libmangenerator import Man
from toomanyfiles import version_date
import gettext

# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work
gettext.install('toomanyfiles', 'locale/po')


def shell(*args):
    print(" ".join(args))
    call(args,shell=True)

def makefile_dist_sources():
    shell("{} setup.py sdist".format(args.python))

def makefile_doc():
    #es
    shell("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/toomanyfiles.pot *.py")
    shell("msgmerge -N --no-wrap -U locale/es.po locale/toomanyfiles.pot")
    shell("msgfmt -cv -o locale/es/LC_MESSAGES/toomanyfiles.mo locale/es.po")

    for language in ["en", "es"]:
        mangenerator(language)

def makefile_install():
    shell("install -o root -d "+ prefixbin)
    shell("install -o root -d "+ prefixlib)
    shell("install -o root -d "+ prefixshare)
    shell("install -o root -d "+ prefixlocale+"/es/LC_MESSAGES/")
    shell("install -o root -d "+ prefixman+"/man1")
    shell("install -o root -d "+ prefixman+"/es/man1")

    shell("install -m 755 -o root toomanyfiles.py "+ prefixbin+"/toomanyfiles")
    shell("install -m 644 -o root locale/es/LC_MESSAGES/toomanyfiles.mo " + mo_es)
    shell("install -m 644 -o root locale/toomanyfiles.en.1 "+ prefixman+"/man1/toomanyfiles.1")
    shell("install -m 644 -o root locale/toomanyfiles.es.1 "+ prefixman+"/es/man1/toomanyfiles.1")

def makefile_uninstall():
    shell("rm " + prefixbin + "/toomanyfiles")
    shell("rm -Rf " + prefixshare)
    shell("rm -Rf " + prefixlib)
    shell("rm " + mo_es)
    shell("rm " + man_en)
    shell("rm " + man_es)

def doxygen():
    os.chdir("doc")
    shell("doxygen Doxyfile")
    os.chdir("..")


def mangenerator(language):
    """
        Create man pages for parameter language
    """
    if language=="en":
        import locale 
        locale.setlocale(locale.LC_ALL,'C')
    else:
        lang1=gettext.translation('toomanyfiles', 'locale', languages=[language])
        lang1.install()
    print("DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

    man=Man("locale/toomanyfiles.{}".format(language))
    man.setMetadata("toomanyfiles",  1,   datetime.date.today(), "Mariano Muñoz", _("Recover normal files and delete files from a partition."))
    man.setSynopsis("[--help] [--version] [--nofiles] [ --nodeleted| --partition| --output ]")

    man.header(_("DESCRIPTION"), 1)
    man.paragraph(_("This app has the following parameters."), 1)
    man.paragraph("--output", 2, True)
    man.paragraph(_("Shows all known devices in database from console."), 3)
    man.save()
    ########################################################################

if __name__ == '__main__':
    start=datetime.datetime.now()
    parser=argparse.ArgumentParser(prog='Makefile.py', description='Makefile in python', epilog=_("Developed by Mariano Muñoz 2018-{}".format(version_date().year)), formatter_class=argparse.RawTextHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--doc', help=_("Generate docs and i18n"),action="store_true",default=False)
    group.add_argument('--doxygen', help=_("Generate doxygen api documentation"), action="store_true", default=False)
    group.add_argument('--install', help=_("Directory to install app. / recomended"), action="store", metavar="PATH", default=None)
    group.add_argument('--uninstall', help=_("Uninstall. / recomended") ,action="store", metavar="PATH", default=None)
    group.add_argument('--dist_sources', help=_("Make a sources tar"), action="store_true",default=False)
    parser.add_argument('--python', help=_("Python path"), action="store",default='/usr/bin/python3')
    args=parser.parse_args()

    if args.install or args.uninstall:
        if args.install:
            destdir=args.install
        elif args.uninstall:
            destdir=args.uninstall

        prefixbin=destdir+"/usr/bin"
        prefixshare=destdir+"/usr/share/toomanyfiles"
        prefixman=destdir+"/usr/share/man"
        prefixlocale=destdir+"/usr/share/locale"
        prefixlib=destdir+"/usr/lib/toomanyfiles"
        mo_es=prefixlocale+"/es/LC_MESSAGES/toomanyfiles.mo"
        man_en=prefixman+"/man1/toomanyfiles.1"
        man_es=prefixman+"/es/man1/toomanyfiles.1"

        if args.install:
            makefile_install()
        if args.uninstall:
            makefile_uninstall()

    elif args.doc==True:
        makefile_doc()
    elif args.dist_sources==True:
        makefile_dist_sources()
    elif args.doxygen==True:
        doxygen()

    print ("*** Process took {} using {} processors ***".format(datetime.datetime.now()-start , cpu_count()))

