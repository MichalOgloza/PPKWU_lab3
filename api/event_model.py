class EventModel:
    def __init__(self, name, date, link):
        self.name = name
        self.date = date
        self.link = link

    def __repr__(self):
        return "EventModel({name}, {date}, {link})".format(name=self.name, date=self.date, link=self.link)
