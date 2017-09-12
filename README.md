# vbdemo


Virtual Boy Demo. Also a test for me to see if I can maintain a complicated source tree.

What this demo will become remains to be seen.

Compilation requires [meson](http://mesonbuild.com), which in turn requires Python
(either the Windows, Cygwin, or POSIX version should work fine). A generic Makefile is
not out of the question in the future, especially if I decide to make the
source VUCC*-compatible as well (which requires rewriting interrupt logic).

A number of options can need to specified to `meson` or `meson configure`. To get
a full list of options, consult `meson_options.txt`.

To configure a build, ensure gccVB (various versions exist on PlanetVB- I use gcc 4.4)
is on the path and run (assuming the working directory is the root of the source
tree):

```
meson.py build --cross-file=cross-file.txt
```

The source tree expects to see the Github-hosted version of [libgccvb](https://github.com/cr1901/libgccvb)
in `./external/libgccvb`, where `.` is the project root. To get it with git,
simply run:

```
git submodule update
```

or download a zip and extract it to that directory.

*Virtual Utopia C Compiler- Nintendo's official Virtual Boy compiler.
