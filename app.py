#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import re
import hashlib, urllib2

from flask import Flask, abort, jsonify, request
from flask import render_template

from urllib import urlopen
from datetime import timedelta
from icalendar import Calendar, Event, vDatetime

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


def convert_to_json(cal):
    data = {}
    data[cal.name] = dict(cal.items())
    data[cal.name]['VEVENT'] = [];
    
    for event in cal.walk():
        if isinstance(event, Event):
            
            uid = event.decoded("UID")
            dtstamp = event.decoded("DTSTAMP")
            start = event.decoded("DTSTART") + LOCAL_TIMEZONE
            end = event.decoded("DTEND") + LOCAL_TIMEZONE
            title = event.decoded("SUMMARY")
            track = event.decoded("LOCATION")
            abstract = ""
            try:
                # seleziono l'url alla descrizione del talk dal parametro ALTREP
                str_to_search = str(event.to_ical().splitlines()[1]) + str(event.to_ical().splitlines()[2][1:])
                _start = 'SUMMARY;ALTREP="'
                _end = '"'
                result = re.search(_start + '(.*)' + _end, str_to_search)
                url_to_scarp = result.group(1)
                
                #..effettuo lo scraping del div con la classe 'cms' dalla pagina
                abstract = url_to_scarp
            except:
                pass;

            # costruisco il dict
            pevent = {}
            #pevent["DTSTAMP"]= dtstamp
            pevent["UID"]= uid
            pevent["ABSTRACT"]= abstract
            pevent["CLASS"] = "PUBLIC"
            pevent["SUMMARY"] = title
            pevent["LOCATION"] = track
            #pevent["ORGANIZER;CN=Python Italia"] = "mailto:info@pycon.it"
            pevent["DTSTART"] = vDatetime(start).to_ical() # start.time().strftime("%Y%m%dT%H%M")
            pevent["GEO"]= ""
            pevent["DTEND"]= vDatetime(end).to_ical() #end.time().strftime("%Y%m%dT%H%M")
            
            data[cal.name]['VEVENT'].append(pevent)
    
    return json.dumps(data, default=date_handler)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-json/<path:url>')
def convert_from_url(url):
    
    ics = get_url_content(url)
    
    hash_value = get_remote_md5_sum(url)
    print "hash_value"
    print (hash_value)
    
    cal = Calendar.from_ical(ics)
    resp = convert_to_json(cal)

    if 'callback' in request.args:
        resp.data = "%s(%s);" % (request.args['callback'], resp.data)
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    #_url ="https://www.pycon.it/en/sprints/schedule/pycon8.ics"
    #convert_from_url(_url)
