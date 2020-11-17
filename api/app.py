import requests
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World!"


@app.route('/calendar')
def get_calendar():
    return requests\
        .get('http://www.weeia.p.lodz.pl/pliki_strony_kontroler/kalendarz.php?rok=2020&miesiac=10&lang=1').content


if __name__ == '__main__':
    app.run(debug=True)
