Title: A primer on apt's mirror:// protocol
Date: 2013-02-23 21:04
Tags: debian, apt
Category: hacks
Slug: apt-mirror
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag

It's sometimes helpful to keep your machines using a list of apt archives
to use, rather then a single mirror, because redudency is good. Rather then
using (the great) services like `http.debian.net` or `ftp.us.debian.org`,
you can set your own mirror lists using apt's `mirror://` protocol.

<aside class="right">
    While initially hacking this through, Micah ended up
    filing a bug on <code>mirror://</code>, more information in
    <a href="http://bugs.debian.org/699310">the bts</a>. I've since been
    able to get it to work for me, but beware!
</aside>

All of this is ultra unstable, so be a bit careful when using this. I've been
using `mirror://` for a few months now, and it seems fine (even have my servers
using it), but it was a bit of a pain to set up. It gets slightly confused if
you point it at something bad, and it's a mild pain to debug. Hopefully
more people will see the value in `mirror://`, and contribute code to it's
development.


Why bother?
===========

If you have a local network mirror, it's helpful to have your machines default
to a local mirror, if you're the sort to keep an archive mirror on the LAN,
and fall back to your nearest friendly mirror otherwise. In addition,
this lets you hand-define where apt searches for mirrors, which is great, since
you can control the subset of servers you ping a bit more closely.


Practical Bits / quickstart
===========================

The following block covers the quick and dirty details on how to set up
`mirror://` for use on your machine (today!). This is very basic, and
details are very sparse, but hopefully there's enough here to help folks
use this on their local system. Basically, you've got three core things to do:

  1. Pick your mirrors (this one's a bit of a duh)
  1. Put them in a public place you can always get to, regardless of
     where you are in cyberspace (I use
     [static.pault.ag](http://static.pault.ag/debian/mirrors.txt)) - remember,
     this is the one thing all your machines need to always get to, no matter
     where they are.
  1. Configure your `sources.list` to use the mirror.txt file by pointing
     to the text file with the `mirror://` protocol.

Turns out `mirror://`'s protocol handler will segfault if you give it
something bad, so don't be afraid if you see `apt-get update` segfault - it
just means you've likely not pointed it at a valid text file. The format of
the text file should be a simple text file of mirrors it can try, in
order of priority. Mine looks a bit like:

    http://127.0.0.1:3142/debian.lcs.mit.edu/debian/
    http://debian.lcs.mit.edu/debian/
    # http://http.debian.net/debian/

Finally, your `sources.list` entry should look a bit like:

    deb mirror://static.pault.ag/debian/mirrors.txt unstable main
    deb mirror://static.pault.ag/debian/mirrors.txt experimental main
    deb-src mirror://static.pault.ag/debian/mirrors.txt unstable main
    deb-src mirror://static.pault.ag/debian/mirrors.txt experimental main

Problems
========


With the good comes the bad. Not everything fully supports this, and most
tools that parse `sources.list` break in a really silly way.


command-not-found
-----------------

`update-command-not-found` will blow up like:


    :::text
    W: Don't know how to handle mirror
    W: Don't know how to handle mirror
    W: Don't know how to handle mirror
    W: Don't know how to handle mirror
    W: Don't know how to handle mirror
    W: Don't know how to handle mirror
