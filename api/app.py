from datetime import datetime

import requests
import arrow
from flask import Flask
from bs4 import BeautifulSoup
from ics import Calendar, Event

from event_model import EventModel

app = Flask(__name__)


@app.route('/')
def home():
    return "This API returns ICS/iCal version of calendar available on http://www.weeia.p.lodz.pl. " \
           "Available at address: /calendar/[year]/[month]"


@app.route('/calendar/current')
def get_current_calendar():
    return get_calendar(datetime.now().year, datetime.now().month)


@app.route('/calendar/<year>/<month>')
def get_calendar(year, month):
    lang = 1
    url = 'http://www.weeia.p.lodz.pl/pliki_strony_kontroler/kalendarz.php?rok={year}&miesiac={month}&lang={lang}'\
        .format(year=year, month=month, lang=lang)

    cal = create_calendar(get_events(url, year, month))
    print(cal)
    return cal.__str__()


def create_calendar(events):
    cal = Calendar()
    for event in events:
        ev = Event()
        ev.name = event.name
        ev.begin = event.date
        ev.created = arrow.utcnow()
        ev.description = event.link
        ev.make_all_day()
        cal.events.add(ev)
    return cal


def get_events(url, year, month):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    events = []
    for td in soup.find_all('td', {"class": "active"}):

        name = td.find('div', {"class": "calendar-text"}).find('div', {"class": "InnerBox"}).find(True).get_text()
        link = td.find('a', {"class": "active"})
        day = link.get_text()
        if len(day) == 1:
            day = "0" + day

        date_string = '{year}-{month}-{day}'.format(year=year, month=month, day=day)
        date = arrow.get(date_string, 'YYYY-MM-DD')
        href = link.get('href')
        if href == "javascript:void();":
            href = ""
        event = EventModel(name, date, href)
        events.append(event)

    return events


if __name__ == '__main__':
    app.run(debug=True)
