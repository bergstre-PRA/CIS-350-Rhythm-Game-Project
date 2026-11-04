from note import Note
class Score:

    TIMING_RANGES: dict[str, tuple[float,float]] = {
        "perfect" : (-0.04, 0.04),
        "great" : (-0.07, 0.07),
        "good" : (-0.1, 0.1),
        "bad" : (-0.125, 0.125)
    }

    ACCURACY_SCORES: dict[str, int] = {
        "perfect" : 300,
        "great" : 100,
        "good" : 50,
        "bad" : 10,
        "miss" : 0
    }



    def __init__(self):
        self.points:int = 0
        self.max_combo:int = 0
        self.combo:int = 0
        self.miss:int = 0
        self.bad:int = 0
        self.good:int = 0
        self.great:int = 0
        self.perfect:int = 0
        self.letterGrade:str = "null"
        self.percentGrade:float = 0.0

    def updateScore(self, note: Note, hitTime: float) -> str:
        self.noteTime = note.hitTime
        self.timing = hitTime - self.noteTime
        return "none"


