class Score:

    SCORE_RANGES = {
        "perfect" : ()
    }

    def __init__(self):
        self.points = 0
        self.max_combo = 0
        self.combo = 0
        self.miss = 0
        self.good = 0
        self.great = 0
        self.perfect = 0
        self.letterGrade = "null"
        self.percentGrade = 0.0

    def updateScore(note, hitTime):
        pass