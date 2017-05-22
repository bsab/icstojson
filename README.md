ICT-to-Json
=========

ICT-to-Json is a simple python/Flask app that consumes iCal data (.ics file) (publicly available at an HTTP URL) and convert it to a JSON format.



Usage
-----

If you prefer to run it directly on your local machine, I suggest using
[virtualenv](https://virtualenv.pypa.io/en/stable/) (maybe have a look at
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/)),
anyway here the commands you have to enter:

    pip install -r requirements.txt
    FLASK_APP=app.py flask run

Now you can browse the API:

    http://0.0.0.0:5000/get-json/http://hostname.com/path/to/file.ics

E.g., let's say we want to get the iCal data available at https://www.pycon.it/p3/schedule/pycon8/app-schedule.ics in JSON format, the URL would look like this:

    http://0.0.0.0:5000/get-json/https://www.pycon.it/p3/schedule/pycon8/app-schedule.ics

The response would look something like this:

```json
{
   "VCALENDAR":{
      "VERSION":"2.0",
      "VEVENT":[
         {
            "SUMMARY":"Apertura / Opening and Startup Competition prize-giving",
            "ORGANIZER;CN=Python Italia":"mailto:info@pycon.it",
            "LOCATION":"All Rooms",
            "STAR":false,
            "DTEND":"20170407T090000",
            "DTSTART":"20170407T084500",
            "GEO":"",
            "CLASS":"PUBLIC",
            "ABSTRACT":"",
            "UID":"https://www.pycon.it/1779"
         },
         {
            "SUMMARY":"Creiamo un'applicazione per la gestione di ticket in Genropy - 240min",
            "ORGANIZER;CN=Python Italia":"mailto:info@pycon.it",
            "LOCATION":"PyTraining",
            "STAR":false,
            "DTEND":"20170408T130000",
            "DTSTART":"20170408T090000",
            "GEO":"",
            "CLASS":"PUBLIC",
            "ABSTRACT":"https://www.pycon.it//conference/talks/creiamo-unapplicazione-per-la-gestione-di-ticket-in-genropy",
            "UID":"https://www.pycon.it/1786"
         }
      ],
      "X-PUBLISHED-TTL":"P0DT1H0M0S",
      "PRODID":"https://www.pycon.it/en/sprints/schedule/pycon8/"
   }
}
```

Deploy to Heroku
---------------

Click on this magic to automatically deploy this app on a free heroku dyno ;) 

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)


Custom installation on Heroku
----------------------

First, install locally (see above). Then:

```
$ heroku create
Creating sab-beyond-7859... done, stack is cedar
http://sab-beyond-7859.herokuapp.com/ | git@heroku.com:sab-beyond-7859.git
Git remote heroku added

$ git push heroku master
Initializing repository, done.
Counting objects: 59, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (52/52), done.
Writing objects: 100% (59/59), 7.95 KiB | 0 bytes/s, done.
Total 59 (delta 21), reused 0 (delta 0)

-----> Python app detected
-----> No runtime.txt provided; assuming python-2.7.6.
-----> Preparing Python runtime (python-2.7.6)
-----> Installing Setuptools (2.1)
-----> Installing Pip (1.5.4)
-----> Installing dependencies using Pip (1.5.4)
...
       Successfully installed Flask Jinja2 Werkzeug gunicorn icalendar pytz distribute
       Cleaning up...
-----> Discovering process types
       Procfile declares types -> web

-----> Compressing... done, 30.6MB
-----> Launching... done, v3
       http://sab-beyond-7859.herokuapp.com/ deployed to Heroku

To git@heroku.com:sab-beyond-7859.git
 * [new branch]      master -> master
```

Done.


Notes
------

Feel free to fork and send a pull request.
