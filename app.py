#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import csv
import json
import re
import hashlib, optparse, urllib2

from datetime import timedelta
from flask import Flask, abort, jsonify, request
from icalendar import Calendar, Event, vDatetime
from urllib import urlopen

app = Flask(__name__)

# ICS files are in GMT; Guidebook has no concept of timezones, it just displays
# whatever time you give it. It makes sense to display in local time of the conference,
# so this variable defines which is the timezone at the time the conference runs.
LOCAL_TIMEZONE = timedelta(hours=2)

def get_remote_md5_sum(url, max_file_size=1024*1024*1024):
    print url
    remote = urlopen(url)
    return hashlib.md5(remote.read()).hexdigest()


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

def get_url_content(url):
    """
    Seleziono il contenuto puntato dall'url, se richiesto
    ritorno anche l'hash sul file remoto
    """
    _hexdigest = None #per fedault non lo calcolo

    if url == 'favicon.ico':
       abort(404)
    if not url.startswith('http'):
       url = 'http://%s' % url
    uh = urllib2.urlopen(url)
    if uh.getcode() != 200:
       abort(404)

    ics = uh.read()
    uh.close()

    return ics;

def convert_pyconfcal_to_json(cal):
    data = {}
    data[cal.name] = dict(cal.items())
    data[cal.name]['VEVENT'] = [];

    for event in cal.walk():
        if isinstance(event, Event):

            uid = event.decoded("UID") if "UID" in event else ""
            dtstamp = event.decoded("DTSTAMP") if "DTSTAMP" in event else ""
            start = (event.decoded("DTSTART") if "DTSTART" in event else "") + LOCAL_TIMEZONE
            end = (event.decoded("DTEND") if "DTEND" in event else "") + LOCAL_TIMEZONE
            title = event.decoded("SUMMARY") if "SUMMARY" in event else ""
            track = event.decoded("LOCATION") if "LOCATION" in event else ""
            description = event.decoded("DESCRIPTION") if "DESCRIPTION" in event else ""
            action = event.decoded("ACTION") if "ACTION" in event else ""

            # costrtuisco il dict
            pevent = {}
            pevent["DTSTAMP"]= dtstamp
            pevent["UID"]= uid
            pevent["CLASS"] = "PUBLIC"
            pevent["SUMMARY"] = title
            pevent["LOCATION"] = track
            pevent["ACTION"] = action
            pevent["DTSTART"] = vDatetime(start).to_ical() # start.time().strftime("%Y%m%dT%H%M")
            pevent["GEO"]= ""
            pevent["DESCRIPTION"] = description
            pevent["DTEND"]= vDatetime(end).to_ical() #end.time().strftime("%Y%m%dT%H%M")

            data[cal.name]['VEVENT'].append(pevent)

    return json.dumps(data, default=date_handler)


@app.route('/')
def index():
    return u'Please use like <code>http://<script>document.write(location.host);</script><noscript>ical2json.pb.io</noscript>/http://www.myserver.com/path/to/file.ics</code><br>Source code and instructions at <a href="https://github.com/bsab/pyconficstojson">https://github.com/bsab/pyconficstojson.git</a>.'

@app.route('/get-json/<path:url>')
def convert_from_url(url):

    ics = get_url_content(url)

    hash_value = get_remote_md5_sum(url)
    print "hash_value"
    print (hash_value)

    cal = Calendar.from_ical(ics)
    resp = convert_pyconfcal_to_json(cal)
    #print resp
    if 'callback' in request.args:
        resp.data = "%s(%s);" % (request.args['callback'], resp.data)
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    #_url ="https://www.pycon.it/en/sprints/schedule/pycon8.ics"
    #convert_from_url(_url)
