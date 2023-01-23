import httpx
from selectolax.parser import HTMLParser

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
        predmety = tree.css(".vyjed")
        for i,predmet in enumerate(predmety):
            znamky = predmet.css(".cislovka")
            vahy = predmet.css(".tab-vaha")[1:]
            for znamka,vaha in zip(znamky,vahy):
                if names[i] not in out.keys():
                    out[names[i]] = []
                out[names[i]].append([znamka.text(), int(vaha.text())])
        return out