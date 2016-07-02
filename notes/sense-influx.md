Title: Hello, Sense!
Date: 2016-07-02 13:13
Tags: python, influxdb, hello, sense
Category: hacks
Slug: hello-influxdb
Author: Paul Tagliamonte
TwitterSite: @paultag
TwitterCreator: @paultag

Last week, I posted about [python-sense](https://notes.pault.ag/hello-sense/),
and API wrapper for the internal Sense API. I wrote this so that I could
pull data about myself into my own databases, allowing me to use that
information for myself.

One way I'm doing this is by pulling my room data into an
[InfluxDB](https://influxdata.com/) database, letting me run time series
queries against my environmental data.

```python
#!/usr/bin/env python

from influxdb import InfluxDBClient

import json
import datetime as dt
from sense.service import Sense

api = Sense()

data = api.room_sensors(quantity=20)

def items(data):
    for flavor, series in data.items():
        for datum in reversed(series):
            value = datum['value']
            if value == -1:
                continue

            timezone = dt.timezone(dt.timedelta(
                seconds=datum['offset_millis'] / 1000,
            ))

            when = dt.datetime.fromtimestamp(
                datum['datetime'] / 1000,
            ).replace(tzinfo=timezone)

            yield flavor, when, value


client = InfluxDBClient(
    'url.to.host.here',
    443,
    'username',
    'password',
    'sense',
    ssl=True,
)


def series(data):
    for flavor, when, value in items(data):
        yield {
            "measurement": "{}".format(flavor),
            "tags": {
                "user": "paultag"
            },
            "time": when.isoformat(),
            "fields": {
                "value": value,
            }
        }


client.write_points(list(series(data)))
```

I'm able to run this on a cron, automatically loading data from the Sense
API into my Influx database. I can then use that with something like
[Grafana](http://grafana.org/), to check out what my room looks like over
time.

![](http://notes.pault.ag/static/posts/hello-influx/sense-influx-light.png)


![](http://notes.pault.ag/static/posts/hello-influx/sense-influx-temp.png)
