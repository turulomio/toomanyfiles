from toomanyfiles import __version__
from setuptools import setup, Command
from mangenerator import Man

import datetime
import gettext
import os
import site

class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/too-many-files/ --delete-after")
        os.chdir("..")

class Video(Command):
    description = "Create video/GIF from console ouput"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.chdir("doc/ttyrec")
        os.system("ttyrecgenerator --output ttyrecgenerator_howto_es 'python3 howto.py --language es' --video")
        os.system("ttyrecgenerator --output ttyrecgenerator_howto_en 'python3 howto.py --language en' --video")
        os.chdir("../..")


class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("rm -Rf {}/toomanyfiles*".format(site.getsitepackages()[0]))
        os.system("rm /usr/bin/toomanyfiles")
        os.system("rm /usr/share/locale/es/LC_MESSAGES/toomanyfiles.mo")
        os.system("rm /usr/share/man/man1/toomanyfiles.1")
        os.system("rm /usr/share/man/es/man1/toomanyfiles.1")

class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/toomanyfiles.pot *.py toomanyfiles/*.py doc/ttyrec/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/toomanyfiles.pot")
        os.system("msgfmt -cv -o locale/es/LC_MESSAGES/toomanyfiles.mo locale/es.po")

        for language in ["en", "es"]:
            self.mangenerator(language)

    def mangenerator(self, language):
        """
            Create man pages for parameter language
        """
        if language=="en":
            gettext.install('toomanyfiles', 'badlocale')
            man=Man("man/man1/toomanyfiles")
        else:
            lang1=gettext.translation('toomanyfiles', 'locale', languages=[language])
            lang1.install()
            man=Man("man/es/man1/toomanyfiles")
        print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

        man.setMetadata("toomanyfiles",  1,   datetime.date.today(), "Mariano Muñoz", _("Remove innecesary files or directories with a date and time pattern in the current directory."))
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

    ########################################################################

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(name='toomanyfiles',
     version=__version__,
     description='Remove files and directories with date and time patterns',
     long_description=long_description,
     long_description_content_type='text/markdown',
     classifiers=['Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                  'Programming Language :: Python :: 3',
                 ], 
     keywords='remove files datetime patterns',
     url='https://too-many-files.sourceforge.io/',
     author='Turulomio',
     author_email='turulomio@yahoo.es',
     license='GPL-3',
     packages=['toomanyfiles'],
     entry_points = {'console_scripts': ['toomanyfiles=toomanyfiles.toomanyfiles:main',
                                        ],
                    },
     data_files=[ ('/usr/share/locale/es/LC_MESSAGES/', ['locale/es/LC_MESSAGES/toomanyfiles.mo']),
                        ('/usr/share/man/man1/', ['man/man1/toomanyfiles.1']), 
                        ('/usr/share/man/es/man1/', ['man/es/man1/toomanyfiles.1'])
               ] , 
     cmdclass={
        'doxygen': Doxygen,
        'doc': Doc,
        'uninstall':Uninstall, 
        'video': Video, 
             },
      zip_safe=False
     )
     
"""
#!/usr/bin/python3
import argparse
import datetime
import os
from subprocess import call
from multiprocessing import cpu_count
from libmangenerator import Man
from toomanyfiles import version_date
import gettext


# I had a lot of problems with UTF-8. LANG must be es_ES.UTF-8 to work
gettext.install('toomanyfiles', 'locale')


def shell(*args):
    print(" ".join(args))
    call(args,shell=True)

def makefile_dist_sources():
    shell("{} setup.py sdist".format(args.python))

def makefile_doc():
    #es
    shell("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/toomanyfiles.pot *.py doc/ttyrec/*.py")
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
    shell("install -m 755 -o root ttyrecgenerator.py "+ prefixbin+"/ttyrecgenerator")
    shell("install -m 755 -o root libttyrecgenerator.py "+ prefixlib+"/libttyrecgenerator.py")
    shell("install -m 644 -o root doc/ttyrec/tty.gif " +  prefixshare + "/demo.gif")
    shell("install -m 644 -o root locale/es/LC_MESSAGES/toomanyfiles.mo " + mo_es)
    shell("install -m 644 -o root locale/toomanyfiles.en.1 "+ prefixman+"/man1/toomanyfiles.1")
    shell("install -m 644 -o root locale/toomanyfiles.es.1 "+ prefixman+"/es/man1/toomanyfiles.1")

def makefile_uninstall():
    shell("rm " + prefixbin + "/toomanyfiles")
    shell("rm " + prefixbin + "/ttyrecgenerator")
    shell("rm -Rf " + prefixshare)
    shell("rm -Rf " + prefixlib)
    shell("rm " + mo_es)
    shell("rm " + man_en)
    shell("rm " + man_es)

def doxygen():
    os.chdir("doc")
    shell("doxygen Doxyfile")
    os.chdir("..")

def video():
    os.chdir("doc/ttyrec")
    shell("ttyrecgenerator --output toomanyfiles_howto_es 'python3 howto.py --language es' --video")
    shell("ttyrecgenerator --output toomanyfiles_howto_en 'python3 howto.py --language en' --video")
    os.chdir("../..")


def mangenerator(language):
        Create man pages for parameter language
    if language=="en":
        gettext.install('toomanyfiles', 'badlocale')
    else:
        lang1=gettext.translation('toomanyfiles', 'locale', languages=[language])
        lang1.install()
    print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

    man=Man("locale/toomanyfiles.{}".format(language))
    man.setMetadata("toomanyfiles",  1,   datetime.date.today(), "Mariano Muñoz", _("Remove innecesary files or directories with a date and time pattern in the current directory."))
                    [--pattern PATTERN] [--disable_log]
                    [--remove_mode {RemainFirstInMonth,RemainLastInMonth}]
                    [--too_young_to_delete TOO_YOUNG_TO_DELETE]
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
    ########################################################################



if __name__ == '__main__':
    start=datetime.datetime.now()
    parser=argparse.ArgumentParser(prog='Makefile.py', description='Makefile in python', epilog=_("Developed by Mariano Muñoz 2018-{}".format(version_date().year)), formatter_class=argparse.RawTextHelpFormatter)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--doc', help=_("Generate docs and i18n"),action="store_true",default=False)
    group.add_argument('--doxygen', help=_("Generate doxygen api documentation"), action="store_true", default=False)
    group.add_argument('--install', help=_("Directory to install app. / recomended"), action="store", metavar="PATH", default=None)
    group.add_argument('--uninstall', help=_("Uninstall. / recomended") ,action="store", metavar="PATH", default=None)
    group.add_argument('--video', help=_("Make a HOWTO video and gif "), action="store_true",default=False)
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
    elif args.video==True:
        video()

    print ("*** Process took {} using {} processors ***".format(datetime.datetime.now()-start , cpu_count()))
"""