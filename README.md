vbdemo
======

Virtual Boy Demo. Also a test for me to see if I can maintain a complicated source tree.

What this demo will become remains to be seen.

Compilation requires SCons, which in turn requires Python (either the Windows, Cygwin, or POSIX version should work fine). 
A generic Makefile is not out of the question in the future, especially if I decide to make the source VUCC*-compatible as 
well (which requires rewriting interrupt logic).

A number of options may need to specified to SCons on the command line (after the program name) for compilation to be successful. To get a full list of options, run:

    scons -h
The file settings.py can be used to store these options permanently. Alternatively, options specified on the command line 
(and by extension the settings file) will be written to a file called variables.cache, and will be read each run. Any 
variable set in settings.py overrides the same variable in variables.cache, while settings.py can be overridden for one 
build by specifying the relevant variable on the command line. 

The source tree expects to see the Github-hosted version of libgccvb in "#/external/libgccvb", where "#" is the project 
root. To get it with git, simply run:

    git submodule update
in "#/external/libgccvb",or download a zip and extract it to that directory.

*Virtual Utopia C Compiler- Nintendo's official Virtual Boy compiler.
