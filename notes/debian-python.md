Title: Musings about Debian and Python
Date: 2013-09-21 22:49
Tags: debian, python
Category: rants
Slug: debian-python
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://notes.pault.ag/static/debian-python.png

On a regular basis, I find myself the odd-man-out when it comes to talking
about how to work with Python on Debian systems. I'm going to write this and
post it so that I might be able to point people at my thoughts without having
to write the same email in response to each thread that pops up.

Turns out I don't fit in with the Debian hardliners (which is to say, the
mindset that `pip` sucks and shouldn't exist), nor do I fit in with the Python
hardliners (which is to say `apt` and `dpkg` are out of date, and neither have
a place on a Development machine).

I think our discourse on this topic has become *petty* and *stupid* in general.
Let's all try to step back and drop a bit of the attitude.

`pip` doesn't suck, and neither does `apt`.
===========================================

The truth is, both sides are wrong. As with any subject, the real
answer here is much more nuanced than either side presents it. I'm going to
try and present my opinion on this, in the way that both my Pythonista self
and my Debianite self see the issue. Hopefully I can keep this short, to
the point, and caked with logic.

The case for `dpkg` (the Debianite in me)
-----------------------------------------

In defense of `dpkg` and `apt`, imagine having to install `python-gnome2`
on all your systems when you install.  It'd be hell on earth.
Imagine having a **user** try to do this. It's insane to assume that
end-users will be using `pip` for this purpose.

`pip` is fun and all, but it's also installing 100% untrusted code to your
system (perhaps as root, if you're using `pip` with `sudo` for some reason),
and hasn't been reviewed for software freeness, which is something Debian
(and Debian users) take seriously. This isn't even to mention the hell that
`pip` wreaks on `dpkg` controlled files / packages.

<aside class="left">
    Remember, Debian spends a lot of time and effort into ensuring software
    is <a href="http://www.debian.org/social_contract#guidelines" >DFSG</a>
    free, and safe.
</aside>

Try to remember how much of your system running (yes, right now) is running
because of Python or Python modules. Try to imagine how much of a pain in
the ass it'd be if you couldn't boot into `GNOME` to use `nm-applet` to connect
to wifi to `pip` install something. I'm sure even the most extreme pip'er
understands the need for Operating System level package management.

Debian also has a bigger problem scope - we're not maintaining a library
in Debian for kicks, we're maintaining it so that *end user applications* may
use the library. When we update something like `Django`, we have to make sure
that we don't break anything using it (although, to be honest, the fact that we
package webapps is an entire rant for later) before we get to update it to the
newest release.

Hell, with a few coffees, I could automate the process of releasing a `.deb`
with a new upstream release, 100% unattended. I won't, however, since this is
an insane idea. Let's go over a brief list of things I do before uploading a
new package:

 1. Review the *entire* codebase for simple mistakes.
 1. Review the *entire* codebase for license issues.
 1. Review the *entire* codebase for files without source, and track down
    (and include source for) any sourceless files (such as `pickle`
    files, etc).
 1. Get to know the upstream, get to know open bugs, write something using
    the lib, in case I need to debug later.
 1. Install the package.
 1. Test the package.
 1. Work out any Debian package issues (this is easy).

Now, a brief list of things I do before I update a package:

<aside class="right">
    Some non-Debian people may call this anal. I disagree, since this is
    important to ensure we have <i>source</i> for all files. In addition,
    it's trivial to take the next step and ensure things are <i>roughly</i>
    safe.
</aside>

 1. Review the changes between the last uploaded version (in diff format, if
    it's sane, otherwise get the VCS and review), ensure all the above are still
    OK.
 1. Review for Debian-local issues (such as how it will upgrade, using
    `piuparts`, and `adequate`, etc).
 1. Check to make sure it won't break any reverse dependencies.
 1. Review for bugfixes that I might need to bring back to the `stable` release.
 1. Figure out if I should (or even can) backport the package, if API is
    stable.
 1. Review for bugs (upstream or in Debian) that I need to mention in the
    debian/changelog.

Clearly, this isn't a quick-and-dirty task. It's not a matter of getting a
package updated (technically), it's a much more detailed process than that.
This is also why Debian is so highly regarded for its technical virtuosity,
and why the
[ISS decided to deploy Debian in space](http://training.linuxfoundation.org/why-our-linux-training/training-reviews/linux-foundation-training-prepares-the-international-space-station-for-linux-migration),
despite other commercial distros such as `Red Hat`, or `Ubuntu`, and
community distros, such as `Fedora` or `Arch`.

<aside class="left">
    Cheap shot, I know.
</aside>

It's also not Debian's job to package the world in the archive. This is an
insane task, and it's not Debian's place to do it. We introduce libraries
as things need them, not because we wrote some new library that someone
may find slightly useful at some point in the future. maybe.

Upstream developers and language communities (not only Python here) tend to
lose sight of why we're doing this in the first place, which
is our users. This isn't some sort of technical pissing contest to see who can
distribute the software in the best way. Debian-folk always keep end users
as our highest priority.

<aside class="right">
    I'm sorry to any
    <a href="http://lists.debian.org/20100106100055.GV3438@radis.liafa.jussieu.fr" >kittens that may have been harmed by this statement</a>.
</aside>

I quote the
[Debian Social Contract](http://www.debian.org/social_contract), when I say
that *Our priorities are our users and free software*. No one's trying to
get *developers* to use `dpkg` to create software. In fact, as you'll see
below, I actively *discourage* using system modules for development.


The case for `pip` (the Pythonista in me)
-----------------------------------------

In defense of `pip`, the idea that Debian will keep the latest versions of
packages is insane. The idea that we can keep pace with upstream releases is
nuts, and the idea that every upstream release on `pypi` is ready to ship is
bananas. [b-a-n-a-n-a-n-a-s](http://youtu.be/gZHjRQjbHrE?t=2m30s).
As a developer, I don't want to support every release, and I surely don't want
other people depending on some random snapshot.

<aside class="right">
    In fact, I have a very hard time saying anything but <i>"try upgrading
    first"</i> when I get a bug report on a side-project.
    It's tough to remember some edge-case from 2 years ago if this code is
    tightly coupled with another codebase.
</aside>

Often times, I'll put stuff up on `pypi` as a preview, or to release often, and
solicit feedback without having to give out instructions on using a `git`
checkout (it's also easier to have them try a version from `pypi` so I can
cross-ref the git tag to reproduce issues when they file them)

<aside class="left">
    Even Debian tools I write, like
    <a href="https://pypi.python.org/pypi/schroot">python-schroot</a>
    are released to <code>pypi</code> first, and I treat that as the
    upstream location when packaging it in Debian.
</aside>

`pypi` is easy, ubiquitous and works regardless of the platform, which means
less of my development time is spent packaging stuff up for platforms I don't
really care about (`Arch`, `Fedora`, `OSX`, `Windows`), even though I value
feedback from users on those systems. The effort it takes to release something
is limited to `python setup.py sdist upload`, and it's in a place (and in a
shape) that anyone can use it without having 10 sets of platform-local
instructions.

Even ignoring all the above, when *I'm* writing a new app or bit of code,
I want to be sure I'm targeting the latest version of the code I depend on,
so that future changes to API won't hit me as hard. By following
along with my dependencies' development, I can be sure that my code breaks
early, and breaks in development, not production. Upstreams also tend to not
like bug reports against old branches, so ensuring I have the latest code from
`pypi` means I can properly file bugs.

Lastly, I prefer `virtualenv` based setups for development, since I'm usually
working on many things at once. This often means version mismatches in
libraries, which brings in API changes (another whole rant here as well).
I *don't* want to keep installing and uninstalling packages to switch between
the two projects, and using a `chroot(8)` means a lot of overhead and that it's
disconnected from my development environment / filesystem, so I resort to
`virtualenv` to isolate my Development environment.

Final notes
===========

<aside class="right">
    I love apt, I love pip, why can't you?
</aside>

I don't want to keep arguing about this. Just accept that the world's a big
place and that there exist use-cases that both `apt` and `pip` need to exist
and work in the way they're working now. At the very least, try and understand
there exist smart people on both sides, and no one is trying to screw anyone
over or keep their own little private club to themselves. Hopefully, going
forward, we can make sure that the integration between these two tools gets
*better*, not worse.

Help make this dream a reality. Contribute to a productive tone, not a
destructive one. In short:

  * Use `pip` without `sudo` always. Don't tell people to use `sudo`.
  * Use `apt` or `dpkg` when deploying system-wide.
  * Understand people are going to package, and they will be more concerned
    about software using your library then keeping your library up to date.
  * Understand Debian Developers and package maintainers have to do a lot of
    work when updating or sponsoring an upload.
  * Understand upstream developers can't be bothered to fix every issue
    with every release (release early, release often) with some snapshot
    you introduced into unstable.
  * Use `pip` and `virtualenv` in development setups, so we can upgrade your
    app when we upgrade the lib.
