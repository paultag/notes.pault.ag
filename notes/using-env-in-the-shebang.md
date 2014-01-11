Title: Using env(1) in the shebang
Date: 2013-01-15 20:02
Tags: unix, posix
Category: hacks
Slug: env-in-shebang
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag

Some of you out there may have tried to pass flags to a script that was being
invoked via `/usr/bin/env` in the shebang (`#!`), such as `python`. You might
recall an error such as:

    :::text
    /usr/bin/env: python -d: No such file or directory

This error is super annoying, so I went about trying to figure out how
I can pass arguments to `python` (or even things like `ipython` or `bpython`).

The idea is we can abuse the concept of a
[polygot](http://en.wikipedia.org/wiki/Polyglot_(computing)) to shim in some
things we care about.


Implementation
==============

Let's take a look at a quick script I hacked up to use bpython with a pre-made
script that drops into interactive work.

    :::text
    #!/bin/sh
    """":
    exec /usr/bin/env bpython -i $0 $@
    """
    import hy
    print "Hython is now importable!"


Let's step through this slowly. First, the bits the `bash` sees:

    :::bash
    #!/bin/sh
    """":
    exec /usr/bin/env bpython -i $0 $@

Which will cause `bpython` to reload the file, which looks like the following
to Python:

    :::python
    #!/bin/sh
    """":
    exec /usr/bin/env bpython -i $0 $@
    """
    import hy
    print "Hython is now importable!"

Where Python can now ignore the docstring. Magic!
