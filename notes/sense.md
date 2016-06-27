Title: Go Debian!
Date: 2016-06-26 21:42
Tags: python, sense, hello.is
Category: hacks
Slug: go-debian
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag

A while back, I saw a [Kickstarter](https://www.kickstarter.com/projects/hello/sense-know-more-sleep-better)
for one of the most well designed and pretty sleep trackers on the market. I
fell in love with it, and it has stuck with me since.

A few months ago, I finally got my hands on one and started to track my data.
Naturally, I now want to store this new data with the rest of the data I have
on myself in my own databases.

I went in search of an API, but I found that the Sense API hasn't been published
yet, and is being worked on by the team. Here's hoping it'll land soon!

After some subdomain guessing, I hit on [api.hello.is](https://api.hello.is).
So, naturally, I went to take a quick look at their Android app and network
traffic, lo and behold, there was a pretty nicely designed API.

This API is clearly an internal API, and as such, it's something that
**should not** be considered stable. However, I'm OK with a fragile API,
so [I've published a quick and dirty API wrapper for the Sense API
to my GitHub.](https://github.com/paultag/python-sense).

I've published it because I've found it useful, but I can't promise the world,
(since I'm not a member of the Sense team at Hello!), so here are a few ground
rules of this wrapper:

 - I make no claims to the stability or completeness.
 - I have no documentation or assurances.
 - I will not provide the client secret and ID. You'll have to find them on
   your own.
 - This may stop working without any notice, and there may even be really nasty
   bugs that result in your alarm going off at 4 AM.
 - Send PRs! This is a side-project for me.


This module is currently Python 3 only. If someone really needs Python 2
support, I'm open to minimally invasive patches to the codebase using
`six` to support Python 2.7.

Working with the API:
---------------------

First, let's go ahead and log in using `python -m sense`.

```
$ python -m sense
Sense OAuth Client ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Sense OAuth Client Secret: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Sense email: paultag@gmail.com
Sense password: 
Attempting to log into Sense's API
Success!
Attempting to query the Sense API
The humidity is **just right**.
The air quality is **just right**.
The light level is **just right**.
It's **pretty hot** in here.
The noise level is **just right**.
Success!
```

Now, let's see if we can pull up information on my Sense:

```python
>>> from sense import Sense
>>> sense = Sense()
>>> sense.devices()
{'senses': [{'id': 'xxxxxxxxxxxxxxxx', 'firmware_version': '11a1', 'last_updated': 1466991060000, 'state': 'NORMAL', 'wifi_info': {'rssi': 0, 'ssid': 'Pretty Fly for a WiFi (2.4 GhZ)', 'condition': 'GOOD', 'last_updated': 1462927722000}, 'color': 'BLACK'}], 'pills': [{'id': 'xxxxxxxxxxxxxxxx', 'firmware_version': '2', 'last_updated': 1466990339000, 'battery_level': 87, 'color': 'BLUE', 'state': 'NORMAL'}]}
```

Neat! Pretty cool. Look, you can even see my WiFi AP! Let's try some more
and pull some trends out.

```python
>>> values = [x.get("value") for x in sense.room_sensors()["humidity"]][:10]
>>> min(values)
45.73904
>>> max(values)
45.985928
>>> 
```

I plan to keep maintaining it as long as it's needed, so I welcome
co-maintainers, and I'd love to see what people build with it! So far, I'm
using it to dump my room data into InfluxDB, pulling information on my room
into Grafana. Hopefully more to come!

Happy hacking!
