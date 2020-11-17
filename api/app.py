import requests
from flask import Flask

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


if __name__ == '__main__':
    app.run(debug=True)
