Title: Automatically lint your packages with debuild.me
Date: 2013-06-09 17:43
Tags: debuild.me, firehose, debian
Category: debian
Slug: debuild-me
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://notes.pault.ag/static/debian.png

Over my time working with Debian packages, I've always been concerned that
I have been missing catchable mistakes by not running all the static checking
tools I could run. As a result, I've been interested in writing some code that
automates this process, a place where I can push a package and come back a few
hours later to check on the results. This is great, since it provides a slightly
less scary interface to new packagers, and helps avoid thinking they've
just been “told off” by a Developer.

I've spent the time to actually write this code, and I've called it
[debuild.me](http://debuild.me). The code itself is in its fourth
iteration, and is built up from a few core components. The client / server code
([lucy](http://github.com/paultag/lucy) and
[ethel](http://github.com/paultag/ethel)) are quite interconnected, but
[firehose](https://github.com/fedora-static-analysis/firehose) works great
on its own, and is a single, unified (and sane!) spec that is easy
to hack with (or even on!). Hopefully, this means that our wrappers will be
usable outside of debuild.me, which is a win for everyone.


Backend Design
==============

The backend ([lucy](http://github.com/paultag/lucy)) was the first part
I wanted to design. I made the decision (very early on) that everything was
going to be 100% Python 3.3+. This lets me use some of the (frankly, sweet)
tools in the stdlib. Since I've written this type of thing before
(I've tried to write this tool [many](https://github.com/paultag/monomoy-old),
[many](https://github.com/paultag/monomoy),
[many](https://github.com/paultag/chatham-old),
[many](https://github.com/paultag/chatham) times before), so I had a rough
sense of how I wanted to design the backend. Past iterations had suffered from
an overly complex server half, so I decided to go ultra minimal with the
design of debuild.me.

<aside class='left'>
  You can find the code for the server (lucy) on
  <a href="http://github.com/paultag/lucy">my GitHub</a>
</aside>

The backend watches a directory (using a simple `inotify` script) and processes
`.changes` files as they come in. If the package is a source package, a set of
jobs are triggered (such as `lintian`, `build` and `desktop-file-validate`),
as well as a different set for binary packages (such as `lintian`, `piuparts`
and `adequite`).  Only people may upload source packages (without any debs) and
only builders can upload binary packages (without source).

The client and server talk using
[XML-RPC](http://docs.python.org/3/library/xmlrpc.server.html) with BASIC HTTP
auth. I'm going to (eventually) SSL secure the transport layer, but for now,
this will work as a proof of concept.

Since I tend to like to keep my codebase simple and straightforward, I've used
[MongoDB](http://www.mongodb.org/) as Lucy's DB. This lets me move between
documents in Mongo to Python objects without any trouble. In addition, I
evaluated some of the queue code out there (ZMQ, etc), and they all seemed
like overkill for my problem, and had a hard time keeping track of jobs that
(must never!) get lost. As a result, I wrote my own (very simple) job queue
in Mongo, which has no sense of scheduling (at all), but can do its job (and
do it well).

Jobs describe what's to be built with a link to the `package` document
that the job relates to, and its `arch` and `suite` (don't worry about the
rest just yet). Jobs get assigned via natural sort on its `UUID` based `_id`,
and assigned to the first builder that can process its `arch` / `suite`.
Source packages are considered `arch:all` / `suite:unstable` (so they always
get the most up-to-date linters on any arch that comes along).

Lucy also allows for uploads to be given an `X-Lucy-Group` tag to manage which
set of packages they're a part of. This comes in handy for doing partial
archive rebuilds, or eventually using it to manage what jobs should be run
on which uploads. This will allow me to run much more time-consuming tools
for packages I want to review versus rebuilding to ensure packages don't
FTBFS or aren't adequite.

Client Design
=============

The buildd client ([ethel](http://github.com/paultag/ethel)) talks with `lucy`
via `XML-RPC` to get assigned new jobs, release old jobs, close finished jobs,
and upload package report data. When the `etheld` requests a new job, it also
passes along what `suites` it knows of, which `arches` it can build, as well
as what `types` it can run (stuff like `lintian`, `build` or `cppcheck`.) Lucy
then assigns the builder to that job (so that we don't allocate the same job
twice), and what time it was assigned at.

<aside class='right'>
  You can find the code for the client (ethel) on
  <a href="http://github.com/paultag/ethel">my GitHub</a>
</aside>

Ethel then takes the result of the job (in the form of a `firehose.model` tree)
and transmits it over the line back to the Lucy server as a `report` (which also
contains information on if the build failed or not), at which point
lucy hands back a location (on the lucy host) that the daemon can write the log
to.

If the job was a binary build, the `etheld` process will `dput` the package to
the server, with a special `X-Lucy-Job` tag to signal which job that build
relates to, so that future lint runs can fetch the `deb` files that the build
produced.

Tooling
=======

Ethel runs a set of static checkers on the source code, which are basically
fancy wrappers around the tools we all know and love (like
[lintian](http://lintian.debian.org/),
[desktop-file-validate](http://freedesktop.org/wiki/Software/desktop-file-utils/),
or [piuparts](http://piuparts.debian.org/)) which output Firehose in place of
home-grown stdout. This allows us to programmatically deal with the output
of these tools in a normal and consistent way.

<aside class='left'>
  You can read more about Firehose over in the Firehose
  <a href="https://github.com/fedora-static-analysis/firehose/blob/master/README.rst">README.rst</a>
</aside>

Some of the more complex runners are made of 3 parts - a `runner`, `wrapper`
and `command`. The server invokes the `command` routine, which invokes the
`runner` (the command just provides a unified interface to all the runners),
who's output gets parsed by the `wrapper` to turn it into a Firehose model
tree.

The goal here is that tons of very quick-running tools get run over a
distributed network, and machine-readable reports get filed in a central
location to aid in reviewing packages.

Ricky
=====

In addition to the actual code to run builds, I've worked on a few tools to
aid with using debuild.me for my DD related life. I have some uncommon
use-cases that are nice to support. One such use-case is the ability to rebuild
packages from the archive (unmodified) to check that they rebuild OK against
the target. This is handy for things like `arch:all` packages that get
uploaded (since they never get rebuilt on the buildd machines, and FTBFSs are
sadly common) or packages that have had a `Build-Dependency` change on them.

Ricky is able to create a `.dsc` url to your friendly local mirror, and fetch
that exact version of the package. Ricky can then also use the `.dsc` (in a
monumental hack) to forge a `package_version_source.changes` file, and sign
it with an autobuild key and upload it to the debuild.me instance. Since it
can also modify the `.changes`'s target distribution, you can also use this to
test if a package will build on `stable` or `testing`, unmodified.

Fred
====

Fred is a wrapper around Ricky, to help with fetching packages that may not
exist yet. Fred also contains an email scraper to read off such lists as
[debian-devel-changes](http://lists.debian.org/debian-devel-changes), and
add an entry to fetch that upload when it becomes available on the local
mirror, pass it to `ricky`, and allow debuild.me to rebuild new packages
that match a set of criteria.

I'm currently playing around with the idea of rebuilding all incoming
Python packages to ensure they don't FTBFS in a clean chroot.


Loofah
======

Loofah is also another wrapper around Ricky, but for use manually. Loofah
is able to sync down the apt `Sources` list, and place it in Mongo for fast
queries. This than allows me to manually run rebuilds on any Source package
that fits a set of critera (written in the form of a Mongo query), which get
pulled and uploaded by `Ricky`.

An example script to rebuild any packages that `Build-Depend` on
`python3-all-dev` in Debian `unstable` / `main` would look like:

<aside class='right'>
    You can find more queries in the Loofah
    <a href = 'https://github.com/paultag/loofah/tree/master/eg' >examples</a>
</aside>

    :::json
    [
        { "version": "unstable", "suite": "main" },
        { "Build-Depends": "python3-all-dev" }
    ]

Or, a script to rebuild any package that depends on CDBS:

    :::json
    [
        {},
        {"$or": [{"Build-Depends": "cdbs"},
                 {"Build-Depends-Indep": "cdbs"}]}
    ]

You can use anything that exists in the `Sources.gz` file to query off of (
including `Maintainer`!)


Future Work
===========

The future work on debuild.me will be centered around making it easier for
buildd nodes to be added to the network, with more and more automation in that
process (likely in the form of debs). I also want to add better control over
the jobs, so that packages I upload only go to my personal servers.

I'd also very much like to get better EC2 / Virtualization support integrated
into the network, so that the buildd count grows with the queue size. This
is a slightly hard problem that I'm keen to fix.

I'm also considering moving the log parsing code *out* of the workers, so that
the parsing code can be fixed without upgrading all the workers. This would also
drop the `Firehose` dep on the client code, which would be nice.

Migration from a debuild.me build into a local `reprepro` repo is something
that would be fairly easy to do as well, likely to be done remotely via
the `XML-RPC` interface, which calls a couple of `reprepro` commands (such as
`includedsc` and `includedeb`) and publishes it to the user's repo. This is
a nice use of the debs that get built, and could also allow debuild.me to be
used like a PPA system, but this allows the user to *not* migrate packages
that may contain `piuparts` issues.
