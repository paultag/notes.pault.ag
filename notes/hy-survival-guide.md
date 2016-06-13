Title: Hy: The survival guide
Date: 2013-08-02 23:19
Tags: hy, lisp
Category: lisp
Slug: hy-survival-guide
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://docs.hylang.org/en/latest/_images/cuddles.png

One of my new favorite languages is a peppy little
[lisp](http://en.wikipedia.org/wiki/Lisp) called
[hy](http://hylang.org). I like it a lot since it's a result of a hilarious
idea I had while talking with some coworkers over Mexican food. Since I'm
the most experienced [Hypster](https://github.com/hylang?tab=members) on the
planet, I figured I should write a survival guide. This will go a lot easier
if you already know Lisp, but you can get away with quite a bit of Python.

The Tao of Hy
=============

We don't have many rules (yet), but we do have quite a bit of philosophy.
The collective Hyve Mind has spent quite a bit of time working out Hy's
internals, and we do spend a bit of time looking at how the language “feels”.
The following is a brief list of some of the design decisions we've
picked out.

  1. Look like a lisp, `DTRT` with it (e.g. dashes turn to underscores,
     earmuffs turn to all-caps.)
  1. We're still Python. Most of the internals translate 1:1 to Python
     internals.
  1. Use unicode *everywhere*.
  1. Tests or it doesn't exist.
  1. Fix the bad decisions in Python 2 when we can (see `true_division`)
  1. When in doubt, defer to Python.
  1. If you're still unsure, defer to Clojure
  1. If you're even more unsure, defer to Common Lisp
  1. Keep in mind we're *not* Clojure. We're *not* Common Lisp. We're Homoiconic
     Python, with extra bits that make sense.

Naturally, this doesn't cover everything, but if you can drop into that mindset,
things start to make quite a bit of sense.



The Style of Hy
===============

Although I am perhaps the least qualified person to do so (I still don't write
idiomatic Lisp all the time), I'm going to set up a few ground-rules when it
comes to idiomatic Hy code. We borrow quite a bit of syntax from Common Lisp
and Clojure, so again, feel free to defer to either if you're not working
on Hy internals. I prefer the
[Clojure Style Guidelines](https://github.com/bbatsov/clojure-style-guide)
myself. As such, these are what we will defer to in the case that the Hy
style is undefined.

Clojure-isms
------------

Hy has quite a few Clojure-isms that I rather prefer, such as the threading
macro, and dot-notation (for accessing methods on an Object), which I would
rather see used throughout the hylands.

    :::clojure
    ;; good:
    (with [fd (open "/etc/passwd")]
        (print (.readlines fd)))

    ;; bad:
    (with [fd (open "/etc/passwd")]
        (print (fd.readlines)))

Some [other hy devs](http://dustycloud.org/) very much disagree, and there's
nothing syntactically invalid about the latter, and it will continue to be
supported (in fact, it makes some things easier!), but it will not be
considered for Hy internal code.

We also very much encourage use of the `threading macro` throughout code
where it makes sense.

    :::clojure
    ;; good:
    (import [sh [cat grep]])
    (-> (cat "/usr/share/dict/words") (grep "-E" "tag$"))
    
    ;; bad:
    (import [sh [cat grep]])
    (grep (cat "/usr/share/dict/words") "-E" "tag$")

However, do use it when it helps aid in clarity, like all things, there are
cases where it makes a mess out of something that ought to not be futzed with.


Python-isms
-----------

In addition to stealing quite a bit of syntax from Clojure, I'm going to
take a few Python rules from PEP8 that apply to Hy as well. These are taken
because PEP8 is a really great set of rules, and Hy code ends up pretty,
well, Pythonic. The following are a collection of Pythonic rules that
explicitly apply to Hy code.

Trailing spaces is a huge one. Never ever ever shall it be OK to have
trailing spaces on internal Hy code. For they suck.

As with Python, you shall always double-space module-level definitions if
separated with a newline.

All public functions must always contain docstrings.

Inline comments shall be *two* spaces from the end of the code, if they
are inline comments. They must always have a space between the comment
character and the start of the comment.


Hy-isms
-------

Indentation shall be two spaces, except where matching the indentation
of the previous line.


    :::clojure
    ;; good (and preferred):
    (defn fib [n]
      (if (<= n 2)
          n
          (+ (fib (- n 1)) (fib (- n 2)))))

    ;; still OK:
    (defn fib [n]
      (if (<= n 2) n (+ (fib (- n 1)) (fib (- n 2)))))

    ;; still OK:
    (defn fib [n]
      (if (<= n 2)
        n
        (+ (fib (- n 1)) (fib (- n 2)))))

    ;; Stupid as hell
    (defn fib [n]
        (if (<= n 2)
                n
          (+ (fib (- n 1)) (fib (- n 2)))))

Parens must *never* be alone, sad, all by their lonesome on their own line.


    :::clojure
    ;; good (and preferred):
    (defn fib [n]
      (if (<= n 2)
          n
          (+ (fib (- n 1)) (fib (- n 2)))))

    ;; Stupid as hell
    (defn fib [n] 
        (if (<= n 2)
          n
          (+ (fib (- n 1)) (fib (- n 2)))
        )
    )  ; GAH, BURN IT WITH FIRE

Don't use S-Expression syntax where vector syntax is really required. For
instance, the fact that:

    :::clojure
    ;; bad (and evil)
    (defn foo (x) (print x))
    (foo 1)

works is just because the compiler isn't overly strict. In reality, the
correct syntax in places such as this is:

    :::clojure
    ;; good (and preferred):
    (defn foo [x] (print x))
    (foo 1)

Notice
======

This guide is, above all, a *guide*. This is also only truly binding
for working on Hy code internally. This post is also super subject to change
in the future, whenever I can be bothered to ensure that we have more of the
de facto rules written down.
