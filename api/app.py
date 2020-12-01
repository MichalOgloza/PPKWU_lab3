import requests
import arrow
from flask import Flask
from bs4 import BeautifulSoup

from event_model import EventModel

app = Flask(__name__)


@app.route('/')
def home():
    return "This API returns ICS/iCal version of calendar available on http://www.weeia.p.lodz.pl. " \
           "Available at address: /calendar/[year]/[month]"


@app.route('/calendar/<year>/<month>')
def get_calendar(year, month):
    lang = 1
    url = 'http://www.weeia.p.lodz.pl/pliki_strony_kontroler/kalendarz.php?rok={year}&miesiac={month}&lang={lang}'\
        .format(year=year, month=month, lang=lang)
    return requests.get(url).content


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

        event = EventModel(name, date, link.get('href'))
        events.append(event)

    return events


if __name__ == '__main__':
    app.run(debug=True)
