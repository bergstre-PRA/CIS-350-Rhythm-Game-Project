from note import Note
class Score:

    TIMING_RANGES: dict[str, float] = {
        "perfect" : 0.016,
        "great" : 0.033,
        "good" : 0.125,
        "bad" : 0.25
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
        self.accuracy: dict[str, int] = {
            "miss" : 0,
            "bad" : 0,
            "good" : 0,
            "great" : 0,
            "perfect" : 0,
        }
        self.letterGrade:str = "F"
        self.percentGrade:float = 1.0

    def _getAccuracy(self, note: Note, hitTime: float) -> str:
        noteTime = note.hitTime
        timing = hitTime - noteTime
        offset = abs(timing)
        score: str

        if offset <= self.TIMING_RANGES["perfect"]:
            score = "perfect"
        elif offset <= self.TIMING_RANGES["great"]:
            score = "great"
        elif offset <= self.TIMING_RANGES["good"]:
            score = "good"
        elif offset <= self.TIMING_RANGES["bad"]:
            score = "bad"
        else:
            score = "miss"
        return score

    def _getAccuracyScore(self, accuracy:str) -> int:
        return self.ACCURACY_SCORES[accuracy]

    def _updateCombo(self, amount:int = 1):
        self.combo += amount
        if self.combo > self.max_combo:
            self.max_combo = self.combo

    def _updateGradePercentage(self) -> float:
            tempScore: float = 0
            maxScore: float = 0
            for name,num in self.accuracy.items():
                tempScore += self._getAccuracyScore(name) * num
                maxScore += self._getAccuracyScore("perfect") * num
    
            self.percentGrade = tempScore / maxScore
            return self.percentGrade

    def _updateLetterGrade(self) -> str:
        percent = self._updateGradePercentage()
        if percent < 0.6:
            self.letterGrade = "F"
        elif percent < 0.7:
            self.letterGrade = "D"
        elif percent < 0.8:
            self.letterGrade = "C"
        elif percent < 0.9:
            self.letterGrade = "B"
        elif percent < 0.97:
            self.letterGrade = "A"
        elif percent < 1:
            self.letterGrade = "S"
        else:
            self.letterGrade = "SS"

        return self.letterGrade


    def addHit(self, note: Note, hitTime: float, multiplier:float = 1):
        accuracy: str = self._getAccuracy(note, hitTime)
        self.accuracy[accuracy] += 1
        if accuracy is "miss" or accuracy is "bad":
            self.combo = 0
        else:
            self._updateCombo()
        self._updateLetterGrade()
        self.points += int(self._getAccuracyScore(accuracy) * multiplier)
        
    

    

    

    



