# TooManyFiles

## Links
    * Source code & Development: https://github.com/Turulomio/toomanyfiles
    * If you use Gentoo you can find a ebuild in https://github.com/Turulomio/myportage/tree/master/app-admin/toomanyfiles

## Description
This command Removes files which names have date and time patterns. You can filter by patterns

## Usage
You can see this animated gif to learn how to use it:
<img src="https://raw.githubusercontent.com/Turulomio/toomanyfiles/master/doc/ttyrec/toomanyfiles_howto_en.gif?raw=true" width="100%"></img>

## Changelog
### 1.0.0
  * Project migrated to poetry>2.0.0
  * Added quality tests
  * Replaced roots by filename patterns. Several patterns can be added.
  * Migrated to pydicts
  * Added --list paramter to see procesed and ignored files, before removing

### 0.5.0
  * Migrated repository from Sourceforge to Github
  * Removed innecesary dependencies in setup.py

### 0.4.0
  * [#11] Print different filename roots in the same directory 
  * [#12] Create static class ExitCodes
  * [#13] Added parameters to main function
  * [#14] Solved bug with directories named with pattern YYYYMMDD HHMM only
  * [#15] Put colored letter output line in a single function
  * Improved --create_examples
  * Added --remove_examples

### 0.3.0
  * Improved output

### 0.2.0
  * Code adapted to ttyrecgenerator-0.6.0

### 0.1.1
  * Corrected image link in README.rst

### 0.1.0
  * Catching exception in gettext
  * Added catalog translations to package
  * Added dependencies to setup.py
  * Removed Makefile.py. Now I'm using setuptools
  * Stable version
  * First version, full functional.
  * Creating infrastructure
