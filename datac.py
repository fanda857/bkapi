from dataclasses import dataclass

@dataclass
class grade:
    grade : float
    weight : int
    def __str__(self) -> str:
        return str(self.grade)

@dataclass
class subject:
    name : str
    date : str
    hour : str
    teacher : str
    room : str
    group : str
    theme : str