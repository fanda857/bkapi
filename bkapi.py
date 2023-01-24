import httpx
from selectolax.parser import HTMLParser
from utils import *
from datac import *

class bkapp:
    def __init__(self, username, password,url):
        self.username = username
        self.password = password
        self.url = url
        self.session = httpx.Client()
    def login(self):
        self.session.post(f"https://{self.url}/Login", data={"username": self.username, "password": self.password})
    def get_grades(self):
        response = self.session.get(f"https://{self.url}/next/prubzna.aspx")
        if response.status_code == 302:
            self.login()
            return self.get_grades()
        tree = HTMLParser(response.text)
        names = [e.css_first("h3").text() for e in tree.css(".predmet-radek")]
        out = {}
        subjects = tree.css(".vyjed")
        for i,subject in enumerate(subjects):
            grades = subject.css(".cislovka")
            weights = subject.css(".tab-vaha")[1:]
            for g,w in zip(grades,weights):
                if names[i] not in out.keys():
                    out[names[i]] = []
                out[names[i]].append(grade(g.text(), int(w.text())))
        return out
    def get_schedule(self):
        out = []
        response = self.session.get(f"https://{self.url}/next/rozvrh.aspx")
        if response.status_code == 302:
            self.login()
            return self.get_schedule()
        tree = HTMLParser(response.text)
        rows = tree.css(".day-row")
        for row in rows:
            srow = []
            items = row.css(".day-item")
            for item in items:
                if item.css_first(".day-item-hover"):
                    srow.append(parse_subject(item.css_first(".day-item-hover").attributes["data-detail"]))
                else:
                    srow.append(None)
            out.append(srow)
        return out