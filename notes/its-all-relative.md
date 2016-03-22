Title: It's all relative: how text can teach us how to handle datetimes
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
and ask them about what they think about timezone handling in their code.
I'll wait. Go ahead.

Rants are funny things. They're fun to watch. Hilarious to give. Sometimes
just getting it all out can help. They can tell you a lot about the true
nature of problems.

It's funny to consider the isomorphic nature of Unicode rants and Timezone
rants.

*I don't think this is an accident.*

I think we can take Ned's framework for dealing with Unicode, and morph it
into something usable for timezones.

Pro Tip #1: U̶n̶i̶c̶o̶d̶e̶ timezone Sandwich
-------------------------------------

Ned's Unicode Sandwich applies -- As early as we can, in the lowest level
we can (reading from the database, filesystem, wherever!), all datetimes
must be timezone qualified with their correct timezone. Always. If you mean
UTC, say it's in UTC.

Treat any unqualified datetimes as "bytes". They're not to be trusted.
[Never, never, never trust 'em](https://youtu.be/W7wpzKvNhfA?t=3m18s). Don't
process any datetimes until you're sure they're in the right timezone.

This lets the delicious inside of your datetime sandwich handle timezones
with grace, and finally, as late as you can, turn it back into bytes
(if at all!).

Most of the time, you don't even have to encode it back to an unqualified
datetime, since modern databases can store datetimes *with* their correct
timezone, without having to turn it into a POSIX Datetime in UTC.

Just like you can declare Unicode strings in your database, and let your
database driver handle the encoding and decoding for you. Avoid losing this
information at all costs. Remember, timezones *are* data! Most of the time,
you want to know what time it was (local time!). If there's a hearing being
held in person, I don't need to know that it's 5:00 AM Eastern, when I really
need to know that it's at 9:00 AM GMT, so I can tell all my British friends to
go and show up.

It's not until you want to show the datetime to the user again should you
consider how to re-encode your datetime to bytes. You should think about
what flavor of bytes, what encoding -- what timezone -- should I be
encoding into?


Pro Tip #2: Know what you have
------------------------------

Is it a few integers that you can claim are a date and a time, or is it a
real, timezone qualified datetime? What timezone?

Always know what bytes you have. Always know what the user *intends* for it
to be. Get information. Any information. Crave information about where
it came from. Remember, encoding is out of band. You need to deduce the
timezone.

Remember, you can't just give up and default to a constant. That will fail.
Don't give up, remember the world uses timezones, and that just because
it's Tuesday doesn't mean it's not Wednesday in another. Or Monday.

Trying to avoid dealing with this will result in the same thing as when you
fail to deal with Unicode - systems will break on input, and they'll break
in hard to fix places. You'll start to play whack-a-mole with `encode` and
`decode`, trying to get the right timezone gymastics in place.


Pro Tip #3: TEST
-----------------

Just like Unicode, testing that your code works with datetimes is important.

Every time I think about how to go about doing this, I think about that
one time that [mjg59](http://mjg59.dreamwidth.org/) couldn't book a flight
starting Tuesday from AKL, landing in HNL on Monday night, because
United couldn't book the last leg to SFO.

Do you ever assume dates only go forward as time goes on? Remember timezones.

Construct hilarious test data, make sure someone in New Zealand's
[+13:45](https://en.wikipedia.org/wiki/UTC%2B13:45) can correctly talk with
their friends in
Baker Island's [-12:00](https://en.wikipedia.org/wiki/UTC%E2%88%9212:00),
and that the events sort right.


Epilogue
--------

Fact of Life #6: Never forget Indiana has 11 timezones. You can never trust
that someone from Indiana isn't giving you EBCDIC.
