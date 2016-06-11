Title: It's all relative
Date: 2016-03-21 23:22
Tags: datetime, timezones, unicode, python
Category: rants
Slug: its-all-relative
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag
TwitterImage: http://notes.pault.ag/static/time.png

As nearly anyone who's worked with me will attest to, I've long since
touted [nedbat's](http://nedbatchelder.com) talk
[Pragmatic Unicode, or, How do I stop the pain?](http://nedbatchelder.com/text/unipain.html)
as one of the most foundational talks, and required watching for all programmers.

The reason is because netbat hits on something bigger - something more
fundemental than how to handle Unicode -- it's how to handle data which is
relative.

For those who want the TL;DR, the argument is as follows:

Facts of Life:

 1. Computers work with Bytes. Bytes go in, Bytes go out.
 2. The world needs more than 256 symbols.
 3. You need both Bytes and Unicode
 4. You cannot infer the encoding of bytes.
 5. Declared encodings can be Wrong

Now, to fix it, the following protips:

 1. [Unicode sandwich](http://nedbatchelder.com/text/unipain/unipain.html#35)
 2. Know what you have
 3. TEST

Relative Data
-------------

I've started to think more about why we do the things we do when we write
code, and one thing that continues to be a source of morbid schadenfreude
is watching code break by failing to handle Unicode right. It's hard! However,
watching *what* breaks lets you gain a bit of insight into how the author
thinks, and what assumptions they make.

When you send someone Unicode, there are a lot of assumptions that have to be
made. Your computer has to trust what you (yes, you!) entered into your web
browser, your web browser has to pass that on over the network (most of the
time without encoding information), to a server which reads that bytestream,
and makes a wild guess at what it should be. That server might save it to a
database, and interoplate it into an HTML template in a different encoding
(called [Mojibake](https://simple.wikipedia.org/wiki/Mojibake)), resulting
in a bad time for everyone involved.

Everything's aweful, and the fact our computers can continue to display
text to us is a goddamn miracle. Never forget that.

When it comes down to it, when I see a byte sitting on a page, I don't know
(and can't know!) if it's `Windows-1252`, `UTF-8`, `Latin-1`, or `EBCDIC`. What's
a poem to me is terminal garbage to you.

Over the years, hacks have evolved. We have
[magic numbers](https://en.wikipedia.org/wiki/Magic_number_(programming)),
and plain ole' hacks to just guess based on the content. Of course, like
all good computer programs, this has lead to its fair share of hilarious
[bugs](https://bugs.launchpad.net/ubuntu/+source/cupsys/+bug/255161/comments/28),
and there's nothing stopping files from (validly!) being multiple things at the
same time.

*Like many things, it's all in the eye of the beholder*.

Timezones
---------

Just like Unicode, this is a word that can put your friendly neighborhood
programmer into a series of profanity laden tirades. Go find one in the wild,
and ask them about what they think about timezone handling bugs they've seen.
I'll wait. Go ahead.

Rants are funny things. They're fun to watch. Hilarious to give. Sometimes
just getting it all out can help. They can tell you a lot about the true
nature of problems.

It's funny to consider the isomorphic nature of Unicode rants and Timezone
rants.

*I don't think this is an accident.*

U̶n̶i̶c̶o̶d̶e̶ timezone Sandwich
-------------------------

Ned's Unicode Sandwich applies -- As early as we can, in the lowest level
we can (reading from the database, filesystem, wherever!), all datetimes
must be timezone qualified with their correct timezone. Always. If you mean
UTC, say it's in UTC.

Treat any unqualified datetimes as "bytes". They're not to be trusted.
[Never, never, never trust 'em](https://youtu.be/W7wpzKvNhfA?t=3m18s). Don't
process any datetimes until you're sure they're in the right timezone.

This lets the delicious inside of your datetime sandwich handle timezones
with grace, and finally, as late as you can, turn it back into bytes
(if at all!). Treat locations as `tzdb` entries, and qualify datetime
objects into their absolute timezone (`EST`, `EDT`, `PST`, `PDT`)

It's not until you want to show the datetime to the user again should you
consider how to re-encode your datetime to bytes. You should think about
what flavor of bytes, what encoding -- what timezone -- should I be
encoding into?

TEST
-----

Just like Unicode, testing that your code works with datetimes is important.
Every time I think about how to go about doing this, I think about that
one time that [mjg59](http://mjg59.dreamwidth.org/) couldn't book a flight
starting Tuesday from AKL, landing in HNL on Monday night, because
United couldn't book the last leg to SFO. Do you ever assume dates only go
forward as time goes on? Remember timezones.

Construct test data, make sure someone in New Zealand's
[+13:45](https://en.wikipedia.org/wiki/UTC%2B13:45) can correctly talk with
their friends in
Baker Island's [-12:00](https://en.wikipedia.org/wiki/UTC%E2%88%9212:00),
and that the events sort right.

Just because it's Noon on New Years Eve in England doesn't mean it's not
1 AM the next year in New Zealand. Places a few miles apart may go on Daylight
savings different days. Indian Standard Time is not even aligned on the hour
to GMT (`+05:30`)!

Test early, and test often. Memorize a few timezones, and challanage
your assumptions when writing code that has to do with time. Don't use
wall clocks to mean monotonic time. Remember there's a whole world out there,
and we only deal with part of it.

It's also worth remembering, as [Andrew Pendleton](https://twitter.com/andrewindc)
pointed out to me, that it's posible that a datetime isn't even *unique* for a
place, since you can never know if `2016-11-06 01:00:00` in `America/New_York`
(in the `tzdb`) is the first one, or second one. Storing `EST` or `EDT` along
with your datetiem may help, though!


Pitfalls
--------

Inproper handling of timezones can lead to some interesting things, and failing
to be explicit (or at least, very rigid) in what you expect will lead to an
unholy class of bugs we've all come to hate. At best, you have confused
users doing math, at worst, someone misses a critical event, or our
security code fails.

I recently found what I regard to be a pretty bad
[bug in apt](https://bugs.debian.org/819697) (which David has prepared a
[fix](https://anonscm.debian.org/cgit/apt/apt.git/diff/?id=9febc2b)
for and is pending upload, yay! Thank you!), which boiled down to documentation
and code expecting datetimes in a timezone, but *accepting any timezone*, and
*silently* treating it as `UTC`.

The solution is to hard-fail, which is an interesting choice to me (as a vocal
fan of timezone aware code), but at the least it won't fail by
misunderstanding what the server is trying to communicate, and I do understand
and empathize with the situation the `apt` maintainers are in.

Final Thoughts
--------------

Overall, my main point is although most modern developers know how to deal
with Uniode pain, I think there is a more general lesson to learn -- namely,
you should always know what data you have, and always remember what it is.
Understand assumptions as early as you can, and always store them with the data.
