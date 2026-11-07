"""Scoring logic for the game."""

from note import Note


class Score:
    """Track combo, accuracy, and score points."""

    TIMING_RANGES: dict[str, float] = {
        "perfect": 0.03,
        "great": 0.1,
        "good": 0.25,
        "bad": 0.4,
    }

    ACCURACY_SCORES: dict[str, int] = {
        "perfect": 300,
        "great": 100,
        "good": 50,
        "bad": 10,
        "miss": 0,
    }

    def __init__(self):
        """Initialize the score tracker."""
        self.points: int = 0
        self.max_combo: int = 0
        self.combo: int = 0
        self.accuracy: dict[str, int] = {
            "miss": 0,
            "bad": 0,
            "good": 0,
            "great": 0,
            "perfect": 0,
        }
        self.letter_grade: str = "F"
        self.percent_grade: float = 1.0

    def _get_accuracy(self, note: Note, hit_time: float) -> str:
        """Determine the timing quality for a note hit."""
        note_time = note.hit_time
        timing = hit_time - note_time
        offset = abs(timing)

        if offset <= self.TIMING_RANGES["perfect"]:
            return "perfect"
        if offset <= self.TIMING_RANGES["great"]:
            return "great"
        if offset <= self.TIMING_RANGES["good"]:
            return "good"
        if offset <= self.TIMING_RANGES["bad"]:
            return "bad"
        return "miss"

    def _get_accuracy_score(self, accuracy: str) -> int:
        """Return the score for accuracy level."""
        return self.ACCURACY_SCORES[accuracy]

    def _update_combo(self, amount: int = 1):
        """Grow the current combo and track the longest one."""
        self.combo += amount
        self.max_combo = max(self.max_combo, self.combo)

    def _update_grade_percentage(self) -> float:
        """Update and return the overall percentage."""
        temp_score: float = 0
        max_score: float = 0
        for name, num in self.accuracy.items():
            temp_score += self._get_accuracy_score(name) * num
            max_score += self._get_accuracy_score("perfect") * num

        self.percent_grade = temp_score / max_score
        return self.percent_grade

    def _update_letter_grade(self) -> str:
        """Update the letter grade based on the current percentage."""
        percent = self._update_grade_percentage()
        if percent < 0.6:
            self.letter_grade = "F"
        elif percent < 0.7:
            self.letter_grade = "D"
        elif percent < 0.8:
            self.letter_grade = "C"
        elif percent < 0.9:
            self.letter_grade = "B"
        elif percent < 0.97:
            self.letter_grade = "A"
        elif percent < 1:
            self.letter_grade = "S"
        else:
            self.letter_grade = "SS"

        return self.letter_grade

    def add_hit(self, accuracy: str, multiplier: float = 1):
        """Add hit to score data."""
        self.accuracy[accuracy] += 1
        if accuracy in {"miss", "bad"}:
            self.combo = 0
        else:
            self._update_combo()
        letter = self._update_letter_grade()
        self.points += int(self._get_accuracy_score(accuracy) * multiplier)

        print("\n\n\n")
        print("combo: " + str(self.combo))
        print("Grade: " + str(letter))
        print("This note: " + str(accuracy))

    def score_hit(self, note: Note, hit_time: float, multiplier: float = 1):
        """Calculate accuracy of note hit and add it."""
        accuracy = self._get_accuracy(note, hit_time)
        self.add_hit(accuracy, multiplier)
