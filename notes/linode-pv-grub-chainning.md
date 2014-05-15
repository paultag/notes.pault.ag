Title: Linode pv-grub chaining
Date: 2014-06-14 19:23
Tags: linode, debian
Category: debian
Slug: linode-pv-grub-chainning
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://notes.pault.ag/static/debian.png

I've been using [Linode](https://linode.com) since 2010, and many of
my friends have heard me talk about how big a fan I am of linode. I've
used Debian unstable on all my Linodes, since I often use them as a remote
shell for general purpose Debian development.

The Problem
===========

Recently, because of my work on [Docker](http://docker.io/), I was forced
to use the Debian kernel, since the stock Linode kernel has no aufs support,
and the default LVM-based Devicemapper backend can be quite a pain.

<aside class="left">
    The btrfs errors are ones I fully expect to be gone soon, I can't wait
    to switch back to using it.
</aside>

I tried loading in [btrfs](http://en.wikipedia.org/wiki/Btrfs) support, and
using that to host the Docker instance backed with btrfs, but it was throwing
errors as well. Stuck with unstable backends, I wanted to use the
[aufs](http://en.wikipedia.org/wiki/Aufs) backend, which, dispite problems in
aufs internally, is quite stable with Docker (and in general).

I started to run through the [Linode Library's guide on PV-Grub](https://library.linode.com/custom-instances/pv-grub-howto),
but that resulted in a cryptic error with xen not understanding the compression
of the kernel. I checked for recent changes to the compresson, and lo, the
Kernel has been switched to use xz compression in sid. Awesome news, really.
XZ compression is awesome, and I've been super impressed with how universally
we've adopted it in Debian. Keep it up!  However, it appears only a newer
pv-grub than Linode has installed will fix this.

After contacting the (ever friendly) Linode support, they were unable to give
me a timeline on adding xz support, which would entail upgrading pv-grub. It
was quite disapointing news, to be honest. Workarounds were suggested,
but I'm not quite happy with them as proper solutions.

After asking in `#debian-kernel`, [waldi](http://bblank.thinkmo.de/blog) was
able to give me a few pointers, and the following is very inspired by him,
the only thing that changed much was config tweaking, which was easy enough.
Thanks, Bastian!


The Constraints
===============

I wanted to maintain a 100% stock configuration from the kernel up.
When I upgraded my kernel, I wanted to just work. I didn't want to
unpack and repack the kernel, and I didn't want to install software
outside main on my system. It had to be 100% Debian and unmodified.


The Solution
============

<aside class="right">
    It's pretty fun to attach to the lish console and watch bootup pass
    through GRUB 0.9, to GRUB 2.x to Linux. Free Software, Fuck Yeah.
</aside>

Left unable to run my own kernel directly in the Linode interface, the tact
here was to use Linode's old pv-grub to chain-load grub-xen, which loaded
a modern kernel. Turns out this works great.

Let's start by creating a config for Linode's pv-grub to read
and use.

    sudo mkdir -p /boot/grub/

Now, since pv-grub is legacy grub, we can write out the following
config to chain-load in `grub-xen` (which is just Grub 2.0, as far as I can
tell) to `/boot/grub/menu.lst`. And to think, I almost forgot all about
`menu.lst`. Almost.

    default 1
    
    timeout 3
    
    title grub-xen shim
    root (hd0)
    kernel /boot/xen-shim
    boot

Just like riding a bike! Now, let's install and set up grub-xen to work for us.

    sudo apt-get install grub-xen
    sudo update-grub

And, let's set the config for the GRUB image we'll create in the next step
in the `/boot/load.cf` file:

    configfile (xen/xvda)/boot/grub/grub.cfg

Now, lastly, let's generate the `/boot/xen-shim` file that we need
to boot to:

    grub-mkimage --prefix '(xen/xvda)/boot/grub' -c /boot/load.cf -O x86_64-xen /usr/lib/grub/x86_64-xen/*.mod > /boot/xen-shim


Next, change your boot configuration to use `pv-grub`, and give the machine
a kick. Should work great! If you run into issues, use the lish shell to
debug it, and let me know what else I should include in this post!

Hack on!
