Title: Docker PostgreSQL Foreign Data Wrapper
Date: 2014-09-18 21:49
Tags: docker, postgresql, fdw, python
Category: python
Slug: dockerfdw
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://notes.pault.ag/static/docker.png

For the tl;dr: [Docker FDW](https://github.com/paultag/dockerfdw) is a thing.
Star it, hack it, try it out. File bugs, be happy. If you want to see what it's
like to read, there's some example SQL down below.

<aside class="left">
    This post was edited on Sep 21st to add information about the
    <code>DELETE</code> and <code>INSERT</code> operators
</aside>

The question is first, what the heck is a PostgreSQL Foreign Data Wrapper?
PostgreSQL Foreign Data Wrappers are plugins that allow C libraries
to provide an adaptor for PostgreSQL to talk to an external database.

Some folks have used this to wrap stuff like
[MongoDB](https://github.com/citusdata/mongo_fdw), which I always found
to be hilarous (and an epic hack).


Enter Multicorn
===============

During my time at [PyGotham](http://pygotham.org/), I saw a talk from 
[Wes Chow](https://twitter.com/weschow) about something called
[Multicorn](http://multicorn.org/). He was showing off some really neat
plugins, such as the git revision history of CPython, and parsed logfiles
from some stuff over at Chartbeat. This basically blew my mind.


<aside class="right">
    If you're interested in some of these, there are a bunch in the
    Multicorn VCS repo, such as the
    <a href="https://github.com/Kozea/Multicorn/blob/master/python/multicorn/gitfdw.py">gitfdw</a>
    example.
</aside>

All throughout the talk I was coming up with all sorts of things that I wanted
to do -- this whole library is basically exactly what I've been dreaming
about for years. I've always wanted to provide a SQL-like interface
into querying API data, joining data cross-API using common crosswalks,
such as using [Capitol Words](http://capitolwords.org/) to query for
Legislators, and use the
[bioguide ids](http://bioguide.congress.gov/biosearch/biosearch.asp)
to `JOIN` against the [congress api](https://sunlightlabs.github.io/congress/)
to get their Twitter account names.

My first shot was to Multicorn the new
[Open Civic Data](http://opencivicdata.org/) API I was working on, chuckled
and put it aside as a really awesome hack.

Enter Docker
============

It wasn't until [tianon](https://github.com/tianon) connected the dots for me
and suggested a [Docker](http://docker.io/) FDW did I get really excited.
Cue a few hours of hacking, and I'm proud to say -- here's
[Docker FDW](https://github.com/paultag/dockerfdw).

This lets us ask all sorts of really interesting questions out of the API,
and might even help folks writing webapps avoid adding too much Docker-aware
logic. Abstractions can be fun!


Setting it up
=============

<aside class="left">
    The only stumbling block you might find (at least on Debian and Ubuntu) is
    that you'll need a Multicorn `.deb`. It's currently undergoing an
    official Debianization from the Postgres team, but in the meantime I put
    the source and binary up on my
    <a href="https://people.debian.org/~paultag/tmp/">people.debian.org</a>.
    Feel free to use that while the Debian PostgreSQL team prepares the upload
    to unstable.
</aside>

I'm going to assume you have a working Multicorn, PostgreSQL and Docker setup
(including adding the `postgres` user to the `docker` group)

So, now let's pop open a `psql` session. Create a database (I called mine
`dockerfdw`, but it can be anything), and let's create some tables.

Before we create the tables, we need to let PostgreSQL know where our
objects are. This takes a name for the `server`, and the `Python` importable
path to our FDW.

```sql
CREATE SERVER docker_containers FOREIGN DATA WRAPPER multicorn options (
    wrapper 'dockerfdw.wrappers.containers.ContainerFdw');

CREATE SERVER docker_image FOREIGN DATA WRAPPER multicorn options (
    wrapper 'dockerfdw.wrappers.images.ImageFdw');
```

Now that we have the server in place, we can tell PostgreSQL to create a table
backed by the FDW by creating a foreign table. I won't go too much into the
syntax here, but you might also note that we pass in some options - these are
passed to the constructor of the FDW, letting us set stuff like the Docker
host.

```sql
CREATE foreign table docker_containers (
    "id"          TEXT,
    "image"       TEXT,
    "name"        TEXT,
    "names"       TEXT[],
    "privileged"  BOOLEAN,
    "ip"          TEXT,
    "bridge"      TEXT,
    "running"     BOOLEAN,
    "pid"         INT,
    "exit_code"   INT,
    "command"     TEXT[]
) server docker_containers options (
    host 'unix:///run/docker.sock'
);


CREATE foreign table docker_images (
    "id"              TEXT,
    "architecture"    TEXT,
    "author"          TEXT,
    "comment"         TEXT,
    "parent"          TEXT,
    "tags"            TEXT[]
) server docker_image options (
    host 'unix:///run/docker.sock'
);
```

And, now that we have tables in place, we can try to learn something about the
Docker containers. Let's start with something fun - a join from containers
to images, showing all image tag names, the container names and the ip of the
container (if it has one!).


```sql
SELECT docker_containers.ip, docker_containers.names, docker_images.tags
  FROM docker_containers
  RIGHT JOIN docker_images
  ON docker_containers.image=docker_images.id;
```

```
     ip      |            names            |                  tags                   
-------------+-----------------------------+-----------------------------------------
             |                             | {ruby:latest}
             |                             | {paultag/vcs-mirror:latest}
             | {/de-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
             | {/ny-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
             | {/ar-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
 172.17.0.47 | {/ms-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
 172.17.0.46 | {/nc-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
             | {/ia-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
             | {/az-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
             | {/oh-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
             | {/va-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
 172.17.0.41 | {/wa-openstates-to-ocd}     | {sunlightlabs/scrapers-us-state:latest}
             | {/jovial_poincare}          | {<none>:<none>}
             | {/jolly_goldstine}          | {<none>:<none>}
             | {/cranky_torvalds}          | {<none>:<none>}
             | {/backstabbing_wilson}      | {<none>:<none>}
             | {/desperate_hoover}         | {<none>:<none>}
             | {/backstabbing_ardinghelli} | {<none>:<none>}
             | {/cocky_feynman}            | {<none>:<none>}
             |                             | {paultag/postgres:latest}
             |                             | {debian:testing}
             |                             | {paultag/crank:latest}
             |                             | {<none>:<none>}
             |                             | {<none>:<none>}
             | {/stupefied_fermat}         | {hackerschool/doorbot:latest}
             | {/focused_euclid}           | {debian:unstable}
             | {/focused_babbage}          | {debian:unstable}
             | {/clever_torvalds}          | {debian:unstable}
             | {/stoic_tesla}              | {debian:unstable}
             | {/evil_torvalds}            | {debian:unstable}
             | {/foo}                      | {debian:unstable}
(31 rows)
```

OK, let's see if we can bring this to the next level now. I finally got around
to implementing `INSERT` and `DELETE` operations, which turned out to be
pretty simple to do. Check this out:

```sql
DELETE FROM docker_containers;
```
```
DELETE 1
```

This will do a `stop` + `kill` after a 10 second hang behind the scenes. It's
actually a lot of fun to spawn up a container and terminate it from
`PostgreSQL`.

```sql
INSERT INTO docker_containers (name, image) VALUES ('hello', 'debian:unstable') RETURNING id;
```

```
                                id                                
------------------------------------------------------------------
 0a903dcf5ae10ee1923064e25ab0f46e0debd513f54860beb44b2a187643ff05

INSERT 0 1
(1 row)
```

Spawning containers works too - this is still very immature and not super
practical, but I figure while I'm showing off, I might as well go all the way.

```sql
SELECT ip FROM docker_containers WHERE id='0a903dcf5ae10ee1923064e25ab0f46e0debd513f54860beb44b2a187643ff05';
```

```
     ip      
-------------
 172.17.0.12
(1 row)
```


Success! This is just a taste of what's to come, so please feel free to hack on
[Docker FDW](https://github.com/paultag/dockerfdw),
tweet me [@paultag](http://twitter.com/paultag), file bugs / feature requests.
It's currently a bit of a hack, and it's something that I think has
long-term potential after some work goes into making sure that this is a rock
solid interface to the Docker API.
