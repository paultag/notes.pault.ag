Title: Hacking a Projector in Hy
Date: 2016-07-31 12:02
Tags: python, hy, pjd5132
Category: hacks
Slug: hacking-a-projector-in-hy
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://docs.hylang.org/en/latest/_images/cuddles.png

About a year ago, I bought a Projector after I finally admitted that I could
actually use a TV in my apartment. I settled on buying a
[ViewSonic PJD5132](http://ap.viewsonic.com/il/products/projectors/PJD5132.php).
It was a really great value, and has been nothing short of a delight to own.

I was always a bit curious about the DB9 connector on the back of the unit,
so I dug into the user manual, and found some hex code strings in there. So,
last year, between my last gig at the
[Sunlight Foundtion](https://sunlightfoundation.com/) and
[USDS](https://www.usds.gov/), I spent some time wandering around the US,
hitting up [DebConf](https://debconf15.debconf.org/), and exploring Washington
DC. Between trips, I set out to figure out exactly what was going on with my
Projector, and see if I could make it do anything fun.

So, I started off with basics, and tried to work out how these command codes
were structured. I had a few working codes, but to write clean code, I'd be
better off understanding why the codes looked like they do. Let's look at
the "Power On" code.

`0x06 0x14 0x00 0x04 0x00 0x34 0x11 0x00 0x00 0x5D`

Some were 10 bytes, other were 11, and most started with similar looking
things. The first byte was usually a `0x06` or `0x07`, followed by two
bytes `0x14 0x00`, and either a `0x04` or `0x05`. Since the first few bytes
were similarly structured, I assumed the first octet (either `0x06` or `0x07`)
was actually a length, since the first 4 octets seemed always present.

So, my best guess is that we have a Length byte at index 0, followed by
two bytes for the Protocol, a flag for if you're Reading or Writing (best
guess on that one), and opaque data following that. Sometimes it's a const
of sorts, and sometimes an octet (either little or big endian, confusingly).

<aside class="left">
  These are all just wild guesses, but thinking of it like this has actually
  helped a bit, so I'm just going to use this as my working understanding
  and adjust as needed.
</aside>

```
Length
 |         Read / Write
 |              |
 |   Protocol   |            Data
 |    |----|    |    |------------------------|
0x06 0x14 0x00 0x04 0x00 0x34 0x11 0x00 0x00 0x5D
```

Right. OK. So, let's get to work. In the spirit of code is data, data is code,
I hacked up some of the projector codes into a s-expression we can use later.
The structure of this is boring, but it'll let us both store the command
code to issue, as well as define the handler to read the data back.

```clojure
(setv *commands*
  ;  function                       type family         control
  '((power-on                         nil nil            (0x06  0x14 0x00  0x04  0x00 0x34 0x11 0x00 0x00 0x5D))
    (power-off                        nil nil            (0x06  0x14 0x00  0x04  0x00 0x34 0x11 0x01 0x00 0x5E))
    (power-status                   const power          (0x07  0x14 0x00  0x05  0x00 0x34 0x00 0x00 0x11 0x00 0x5E))
    (reset                            nil nil            (0x06  0x14 0x00  0x04  0x00 0x34 0x11 0x02 0x00 0x5F))
    ...
```

As well as defining some of the const responses that come back from the
Projector itself. These are pretty boring, but it's helpful to put a
name to the int that falls out.

```clojure
(setv *consts*
  '((power        ((on           (0x00 0x00 0x01))
                   (off          (0x00 0x00 0x00))))

    (freeze       ((on           (0x00 0x00 0x01))
                   (off          (0x00 0x00 0x00))))
	...
```

After defining a few simple functions to write the byte arrays to the serial
port as well as reading and understanding responses from the projector, I could
start elaborating on some higher order functions that can talk projector. So
the first thing I wrote was to make a function that converts the command
entry into a native Hy function.

```clojure
(defn make-api-function [function type family data]
  `(defn ~function [serial]
      (import [PJD5132.dsl [interpret-response]]
              [PJD5132.serial [read-response/raw]])
      (serial.write (bytearray [~@data]))
      (interpret-response ~(str type) ~(str family) (read-response/raw serial))))
```

Fun. Fun! Now, we can invoke it to create a Hy & Python importable API wrapper
in a few lines!

```clojure
(import [PJD5132.commands [*commands*]]
        [PJD5132.dsl [make-api-function]])

(list (map (fn [(, function type family command)]
               (make-api-function function type family command)) *commands*)))
```

Cool. So, now we can import things like `power-on` from `*commands*` which
takes a single argument (`serial`) for the serial port, and it'll send a
command, and return the response. The best part about all this is you only
have to define the data once in a list, and the rest comes for free.

Finally, I do want to be able to turn my projector on and off over the network
so I went ahead and make a Flask "API" on top of this. First, let's define
a macro to define Flask routes:

```clojure
(defmacro defroute [name root &rest methods]
  (import os.path)

  (defn generate-method [path method status]

    `(with-decorator (app.route ~path) (fn []
       (import [PJD5132.api [~method ~(if status status method)]])

       (try (do (setv ret (~method serial-line))
               ~(if status `(setv ret (~status serial-line)))
                (json.dumps ret))
       (except [e ValueError]
          (setv response (make-response (.format "Fatal Error: ValueError: {}" (str e))))
          (setv response.status-code 500)
          response)))))

  (setv path (.format "/projector/{}" name))
  (setv actions (dict methods))
  `(do ~(generate-method path root nil)
       ~@(list-comp (generate-method (os.path.join path method-path) method root)
                    [(, method-path method) methods])))
```

Now, we can define how we want our API to look, so let's define the `power`
route, which will expand out into the Flask route code above.

```clojure
(defroute power
  power-status
  ("on"  power-on)
  ("off" power-off))
```

And now, let's play with it!

```
$ curl http://192.168.1.50/projector/power
"off"
$ curl http://192.168.1.50/projector/power/on
"on"
$ curl http://192.168.1.50/projector/power
"on"
```

Or, the volume!

```
$ curl 192.168.1.50/projector/volume
10
$ curl 192.168.1.50/projector/volume/decrease
9
$ curl 192.168.1.50/projector/volume/decrease
8
$ curl 192.168.1.50/projector/volume/decrease
7
$ curl 192.168.1.50/projector/volume/increase
8
$ curl 192.168.1.50/projector/volume/increase
9
$ curl 192.168.1.50/projector/volume/increase
10
```

Check out the full source over at [github.com/paultag/PJD5132](https://github.com/paultag/PJD5132/)!
