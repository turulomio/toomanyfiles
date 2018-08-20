Source code & Development:
    https://sourceforge.net/projects/too-many-files/
Doxygen documentation:
    http://turulomio.users.sourceforge.net/doxygen/too-many-files/
Main developer web page:
    http://turulomio.users.sourceforge.net/en/proyectos.html
Gentoo ebuild
    You can find a Gentoo ebuild in https://sourceforge.net/p/xulpymoney/code/HEAD/tree/myportage/app-admin/toomanyfiles/

Description
===========
Removes files which name has date and time patterns

License
=======
GPL-3

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.
* https://pypi.org/project/mangenerator/, to generate man files.
* https://pypi.org/project/ttyrecgenerator/, to generate animated gifs.

Usage
=====
You can see this animated gif to learn how to use it:

.. image:: https://sourceforge.net/p/too-many-files/code/HEAD/tree/doc/ttyrec/toomanyfiles_howto_en.gif?format=raw
   :height: 800px
   :width: 600px
   :scale: 100 %
   :align: center

Changelog
=========
X.X.X
  * [#12] Create static class ExitCodes
  * [#13] Added parameters to main function
  * [#15] Put colored letter output line in a single function
0.3.0
  * Improved output
0.2.0
  * Code adapted to ttyrecgenerator-0.6.0
0.1.1
  * Corrected image link in README.rst
0.1.0
  * Catching exception in gettext
  * Added catalog translations to package
  * Added dependencies to setup.py
  * Removed Makefile.py. Now I'm using setuptools
  * Stable version
  * First version, full functional.
  * Creating infrastructure
