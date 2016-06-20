Title: Go Debian!
Date: 2016-06-19 12:30
Tags: golang, debian
Category: hacks
Slug: go-debian
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://notes.pault.ag/static/debian.png

As some of the world knows full well by now, I've been noodling with Go
for a few years, working through its pros, its cons, and thinking a lot
about how humans use code to express thoughts and ideas. Go's got a lot of
neat use cases, suited to particular problems, and used in the right place,
you can see some clear massive wins.

<aside class="left">
Some of the things Go is great at: Writing a server. Dealing with asynchronous
communication. Backend and front-end in the same binary. Fast and memory safe.
</aside>

<aside class="right">
Things Go is bad at: Having to rebuild everything for a CVE. Having if
`err != nil` everywhere. "Better than C" being the excuse for bad semantics.
No generics, cgo (enough said)
</aside>

I've started writing Debian tooling in Go, because it's a pretty natural fit.
Go's fairly tight, and overhead shouldn't be taken up by your operating system.
After a while, I wound up hitting the usual blockers, and started to build up
abstractions. They became pretty darn useful, so, this blog post is announcing
(a still incomplete, year old and perhaps API changing) Debian package for Go.
The Go importable name is `pault.ag/go/debian`. This contains a lot of utilities
for dealing with Debian packages, and will become an edited down "toolbelt"
for working with or on Debian packages.

# Module Overview

Currently, the package contains 4 major sub packages. They're a `changelog`
parser, a `control` file parser, `deb` file format parser, `dependency` parser
and a `version` parser. Together, these are a set of powerful building blocks
which can be used together to create higher order systems with reliable
understandings of the world.

## changelog

The first (and perhaps most incomplete and least tested) is a [changelog file
parser.](https://godoc.org/pault.ag/go/debian/changelog). This provides the
programmer with the ability to pull out the suite being targeted in the
changelog, when each upload was, and the version for each. For example, let's
look at how we can pull when all the uploads of Docker to sid took place:

```go
func main() {
	resp, err := http.Get("http://metadata.ftp-master.debian.org/changelogs/main/d/docker.io/unstable_changelog")
	if err != nil {
		panic(err)
	}
	allEntries, err := changelog.Parse(resp.Body)
	if err != nil {
		panic(err)
	}
	for _, entry := range allEntries {
		fmt.Printf("Version %s was uploaded on %s\n", entry.Version, entry.When)
	}
}
```
The output of which looks like:

```
Version 1.8.3~ds1-2 was uploaded on 2015-11-04 00:09:02 -0800 -0800
Version 1.8.3~ds1-1 was uploaded on 2015-10-29 19:40:51 -0700 -0700
Version 1.8.2~ds1-2 was uploaded on 2015-10-29 07:23:10 -0700 -0700
Version 1.8.2~ds1-1 was uploaded on 2015-10-28 14:21:00 -0700 -0700
Version 1.7.1~dfsg1-1 was uploaded on 2015-08-26 10:13:48 -0700 -0700
Version 1.6.2~dfsg1-2 was uploaded on 2015-07-01 07:45:19 -0600 -0600
Version 1.6.2~dfsg1-1 was uploaded on 2015-05-21 00:47:43 -0600 -0600
Version 1.6.1+dfsg1-2 was uploaded on 2015-05-10 13:02:54 -0400 EDT
Version 1.6.1+dfsg1-1 was uploaded on 2015-05-08 17:57:10 -0600 -0600
Version 1.6.0+dfsg1-1 was uploaded on 2015-05-05 15:10:49 -0600 -0600
Version 1.6.0+dfsg1-1~exp1 was uploaded on 2015-04-16 18:00:21 -0600 -0600
Version 1.6.0~rc7~dfsg1-1~exp1 was uploaded on 2015-04-15 19:35:46 -0600 -0600
Version 1.6.0~rc4~dfsg1-1 was uploaded on 2015-04-06 17:11:33 -0600 -0600
Version 1.5.0~dfsg1-1 was uploaded on 2015-03-10 22:58:49 -0600 -0600
Version 1.3.3~dfsg1-2 was uploaded on 2015-01-03 00:11:47 -0700 -0700
Version 1.3.3~dfsg1-1 was uploaded on 2014-12-18 21:54:12 -0700 -0700
Version 1.3.2~dfsg1-1 was uploaded on 2014-11-24 19:14:28 -0500 EST
Version 1.3.1~dfsg1-2 was uploaded on 2014-11-07 13:11:34 -0700 -0700
Version 1.3.1~dfsg1-1 was uploaded on 2014-11-03 08:26:29 -0700 -0700
Version 1.3.0~dfsg1-1 was uploaded on 2014-10-17 00:56:07 -0600 -0600
Version 1.2.0~dfsg1-2 was uploaded on 2014-10-09 00:08:11 +0000 +0000
Version 1.2.0~dfsg1-1 was uploaded on 2014-09-13 11:43:17 -0600 -0600
Version 1.0.0~dfsg1-1 was uploaded on 2014-06-13 21:04:53 -0400 EDT
Version 0.11.1~dfsg1-1 was uploaded on 2014-05-09 17:30:45 -0400 EDT
Version 0.9.1~dfsg1-2 was uploaded on 2014-04-08 23:19:08 -0400 EDT
Version 0.9.1~dfsg1-1 was uploaded on 2014-04-03 21:38:30 -0400 EDT
Version 0.9.0+dfsg1-1 was uploaded on 2014-03-11 22:24:31 -0400 EDT
Version 0.8.1+dfsg1-1 was uploaded on 2014-02-25 20:56:31 -0500 EST
Version 0.8.0+dfsg1-2 was uploaded on 2014-02-15 17:51:58 -0500 EST
Version 0.8.0+dfsg1-1 was uploaded on 2014-02-10 20:41:10 -0500 EST
Version 0.7.6+dfsg1-1 was uploaded on 2014-01-22 22:50:47 -0500 EST
Version 0.7.1+dfsg1-1 was uploaded on 2014-01-15 20:22:34 -0500 EST
Version 0.6.7+dfsg1-3 was uploaded on 2014-01-09 20:10:20 -0500 EST
Version 0.6.7+dfsg1-2 was uploaded on 2014-01-08 19:14:02 -0500 EST
Version 0.6.7+dfsg1-1 was uploaded on 2014-01-07 21:06:10 -0500 EST
```

## control

Next is one of the most complex, and one of the oldest parts of `go-debian`,
which is the [control file parser](https://godoc.org/pault.ag/go/debian/control)
(otherwise sometimes known as `deb822`). This module was inspired by the way
that the `json` module works in Go, allowing for files to be defined in code
with a `struct`. This tends to be a bit more declarative, but also winds up
putting logic into struct tags, which can be a nasty anti-pattern if used too
much.

The first primitive in this module is the concept of a `Paragraph`, a struct
containing two values, the order of keys seen, and a map of `string` to `string`.
All higher order functions dealing with control files will go through this
type, which is a helpful interchange format to be aware of. All parsing of
meaning from the Control file happens when the Paragraph is unpacked into
a struct using reflection.

The idea behind this strategy that you define your struct, and let the Control
parser handle unpacking the data from the IO into your container, letting you
maintain type safety, since you never have to read and cast, the conversion
will handle this, and return an Unmarshaling error in the event of failure.

<aside class="right">
I'm starting to think parsing and defining the control structs are two different
tasks and should be split apart -- or the common structs ought to be removed
entirely. More on this later.
</aside>

Additionally, Structs that define an anonymous member of `control.Paragraph`
will have the raw `Paragraph` struct of the underlying file, allowing the
programmer to handle dynamic tags (such as `X-Foo`), or at least, letting
them survive the round-trip through go.

The default [decoder](https://godoc.org/pault.ag/go/debian/control#NewDecoder)
contains an argument, the ability to verify the input control file using an
OpenPGP keyring, which is exposed to the programmer through the
`(*Decoder).Signer()` function. If the passed argument is nil, it will not
check the input file signature (at all!), and if it has been passed, any
signed data must be found or an `error` will fall out of the `NewDecoder` call.
On the way out, the opposite happens, where the struct is introspected,
turned into a `control.Paragraph`, and then written out to the `io.Writer`.

Here's a quick (and VERY dirty) example showing the basics of reading and
writing Debian Control files with `go-debian`.

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"strings"

	"pault.ag/go/debian/control"
)

type AllowedPackage struct {
	Package     string
	Fingerprint string
}

func (a *AllowedPackage) UnmarshalControl(in string) error {
	in = strings.TrimSpace(in)
	chunks := strings.SplitN(in, " ", 2)
	if len(chunks) != 2 {
		return fmt.Errorf("Syntax sucks: '%s'", in)
	}
	a.Package = chunks[0]
	a.Fingerprint = chunks[1][1 : len(chunks[1])-1]

	return nil
}

type DMUA struct {
	Fingerprint     string
	Uid             string
	AllowedPackages []AllowedPackage `control:"Allow" delim:","`
}

func main() {
	resp, err := http.Get("http://metadata.ftp-master.debian.org/dm.txt")
	if err != nil {
		panic(err)
	}

	decoder, err := control.NewDecoder(resp.Body, nil)
	if err != nil {
		panic(err)
	}

	for {
		dmua := DMUA{}
		if err := decoder.Decode(&dmua); err != nil {
			if err == io.EOF {
				break
			}
			panic(err)
		}
		fmt.Printf("The DM %s is allowed to upload:\n", dmua.Uid)
		for _, allowedPackage := range dmua.AllowedPackages {
			fmt.Printf("   %s [granted by %s]\n", allowedPackage.Package, allowedPackage.Fingerprint)
		}
	}
}
```

Output (truncated!) looks a bit like:

```
...
The DM Allison Randal <allison@lohutok.net> is allowed to upload:
   parrot [granted by A4F455C3414B10563FCC9244AFA51BD6CDE573CB]
...
The DM Benjamin Barenblat <bbaren@mit.edu> is allowed to upload:
   boogie [granted by 3224C4469D7DF8F3D6F41A02BBC756DDBE595F6B]
   dafny [granted by 3224C4469D7DF8F3D6F41A02BBC756DDBE595F6B]
   transmission-remote-gtk [granted by 3224C4469D7DF8F3D6F41A02BBC756DDBE595F6B]
   urweb [granted by 3224C4469D7DF8F3D6F41A02BBC756DDBE595F6B]
...
The DM أحمد المحمودي <aelmahmoudy@sabily.org> is allowed to upload:
   covered [granted by 41352A3B4726ACC590940097F0A98A4C4CD6E3D2]
   dico [granted by 6ADD5093AC6D1072C9129000B1CCD97290267086]
   drawtiming [granted by 41352A3B4726ACC590940097F0A98A4C4CD6E3D2]
   fonts-hosny-amiri [granted by BD838A2BAAF9E3408BD9646833BE1A0A8C2ED8FF]
   ...
...
```

## deb

Next up, we've got the `deb` module. This contains code to handle reading
Debian 2.0 `.deb` files. It contains a wrapper that will parse the control
member, and provide the data member through the
[archive/tar](https://godoc.org/archive/tar) interface.

Here's an example of how to read a `.deb` file, access some metadata, and
iterate over the `tar` archive, and print the filenames of each of the
entries.

```go
func main() {
	path := "/tmp/fluxbox_1.3.5-2+b1_amd64.deb"
	fd, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer fd.Close()

	debFile, err := deb.Load(fd, path)
	if err != nil {
		panic(err)
	}

	version := debFile.Control.Version
	fmt.Printf(
		"Epoch: %d, Version: %s, Revision: %s\n",
		version.Epoch, version.Version, version.Revision,
	)

	for {
		hdr, err := debFile.Data.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}
		fmt.Printf("  -> %s\n", hdr.Name)
	}
}
```

Boringly, the output looks like:

```
Epoch: 0, Version: 1.3.5, Revision: 2+b1
  -> ./
  -> ./etc/
  -> ./etc/menu-methods/
  -> ./etc/menu-methods/fluxbox
  -> ./etc/X11/
  -> ./etc/X11/fluxbox/
  -> ./etc/X11/fluxbox/window.menu
  -> ./etc/X11/fluxbox/fluxbox.menu-user
  -> ./etc/X11/fluxbox/keys
  -> ./etc/X11/fluxbox/init
  -> ./etc/X11/fluxbox/system.fluxbox-menu
  -> ./etc/X11/fluxbox/overlay
  -> ./etc/X11/fluxbox/apps
  -> ./usr/
  -> ./usr/share/
  -> ./usr/share/man/
  -> ./usr/share/man/man5/
  -> ./usr/share/man/man5/fluxbox-style.5.gz
  -> ./usr/share/man/man5/fluxbox-menu.5.gz
  -> ./usr/share/man/man5/fluxbox-apps.5.gz
  -> ./usr/share/man/man5/fluxbox-keys.5.gz
  -> ./usr/share/man/man1/
  -> ./usr/share/man/man1/startfluxbox.1.gz
...
```

## dependency

The `dependency` package provides an interface to parse and compute
dependencies. This package is a bit odd in that, well, there's no other
library that does this. The issue is that there are actually two different
parsers that compute our Dependency lines, one in Perl (as part of `dpkg-dev`)
and another in C (in `dpkg`).

<aside class="left">
I have yet to track it down, but it's shockingly likely that `apt` has another
in `C++`, and maybe another in `aptitude`. I don't know this for a fact, so
I'll assume nothing
</aside>

To date, this has resulted in me filing
[three](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=816473)
[different](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=784808)
[bugs](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=784806).
I also found a broken package in the
[archive](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=816741),
which actually resulted in another bug being (totally accidentally)
[already fixed](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=815478).
I hope to continue to run the archive through my parser in hopes of finding
more bugs! This package is a bit complex, but it basically just returns what
amounts to be an [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
for our Dependency lines. I'm positive there are bugs, so file them!

```go
func main() {
	dep, err := dependency.Parse("foo | bar, baz, foobar [amd64] | bazfoo [!sparc], fnord:armhf [gnu-linux-sparc]")
	if err != nil {
		panic(err)
	}

	anySparc, err := dependency.ParseArch("sparc")
	if err != nil {
		panic(err)
	}

	for _, possi := range dep.GetPossibilities(*anySparc) {
		fmt.Printf("%s (%s)\n", possi.Name, possi.Arch)
	}
}
```

Gives the output:

```
foo (<nil>)
baz (<nil>)
fnord (armhf)
```

## version

Right off the bat, I'd like to thank
[Michael Stapelberg](https://twitter.com/zekjur) for letting me graft this
out of [dcs](https://github.com/debian/dcs) and into the `go-debian` package.
This was nearly entirely his work (with a one or two line function I added
later), and was amazingly helpful to have. Thank you!

This module implements Debian version comparisons and parsing, allowing for
sorting in lists, checking to see if it's native or not, and letting the
programmer to implement smart(er!) logic based on upstream (or Debian)
version numbers.

This module is extremely easy to use and very straightforward, and not worth
writing an example for.

# Final thoughts

This is more of a "Yeah, OK, this has been useful enough to me at this point
that I'm going to support this" rather than a "It's stable!" or even
"It's alive!" post. Hopefully folks can report bugs and help iterate on
this module until we have some really clean building blocks to build
solid higher level systems on top of. Being able to have multiple libraries
interoperate by relying on `go-debian` will be a massive ease.
I'm in need of more documentation, and to finalize some parts of the older
sub package APIs, but I'm hoping to be at a "1.0" real soon now.
