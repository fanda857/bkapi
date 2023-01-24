import json
from datac import *
def parse_grade(grade):
    if "-" in grade:
        return float(grade.split("-")[0])+0.5
    else:
        try:
            return float(grade)
        except ValueError:
            return 5
        
def parse_subject(text):
    js = json.loads(text)
    t = js["type"]
    if t == "atom":
        s,date = js["subjecttext"].split(" | ")[:-1]
        teacher = js["teacher"]
        room = js["room"]
        group = js["group"] if js["group"] != "" else None
        theme = js["theme"] if js["theme"] != "" else None
        return subject(s,date,teacher,room,group,theme)
    else:
        return None
    