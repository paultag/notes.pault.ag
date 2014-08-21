Title: A treatise on Linux Daemons
Date: 2014-08-21 15:40
Tags: debian, daemon
Category: debian
Slug: daemons-on-linux
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://notes.pault.ag/static/debian.png

Far too often people tend to be confused by the process and theory behind
the act of daemonizing a service under Linux. This post will cover the basics
of writing a daemon, common "gotchas", and practical notes about deployment
with regards to init systems.


Hello, World
============

So, let's start from the beginning.
[Daemons](http://en.wikipedia.org/wiki/Daemon_(computing)) are background
services that preform tasks behind the scenes. A common meme in naming daemons
is appending "d" to the project name.
Daemons commonly expose a service into userland or over the network, or
preform periodic tasks. Stuff like a webservers (such as
[httpd](http://httpd.apache.org/) or
[nginx](http://nginx.org/)) listen to incoming `http` requests, commonly
on port 80, and respond to the clients.


Anatomy of a Daemon
===================


Creating a Daemon
=================

C
-

Python
------


Go
--


Common Daemon Tricks
====================


Setting up a Daemon to run
==========================


Debian and Ubuntu-specific notes
================================
