from pathlib import Path
from typing import TypedDict, NotRequired, TypeAlias
import json

ASSETS_DIR = Path(__file__).parent.parent / "Assets"
SONGS_DIR = ASSETS_DIR / "Songs"
CHARTS_DIR = ASSETS_DIR / "Chart Files"



class ChartNote(TypedDict):
    beat: float
    length: float
    hitTime: NotRequired[float]


class ChartFile(TypedDict):
    name: str
    bpm: float
    charts: dict[str, list[ChartNote]]

Chart: TypeAlias = dict[str, ChartFile | bool]

_cachedCharts: Chart = {}


def find_song(name:str) -> Path | bool:
    for file in SONGS_DIR.iterdir():
        if file.is_file() and file.name == str(name) + ".mp3":
            return file
    return False

#checks if chart file exists and returns it
def getChartFile(name:str) -> Path | bool:
    for file in CHARTS_DIR.iterdir():
            if file.is_file() and file.name == str(name) + ".json":
                return file
    return False

#retrieves data from chart json, caches already loaded data
def getChartData(name:str) -> ChartFile | bool:
    if name in _cachedCharts:
        return _cachedCharts[name]

    chart = getChartFile(name)
    if chart is False:
        return False
    
    with open(chart, "r") as file:
        data = json.load(file)
    _cachedCharts[name] = data
    return data

#retrieve song name from chart
def getSongName(name: str) -> str | bool:
    data = getChartData(name)
    if isinstance(data, bool):
        return False
    
    return data["name"]

#retrieve song bpm from chart
def getBpm(name: str) -> float | bool:
    data = getChartData(name)
    if isinstance(data, bool):
        return False
    
    return data["bpm"]

#Converts a beat number to a timestamp in seconds.
#beat_one_at_zero=True: Beat 1 occurs at 0.0 seconds.
def beatToSeconds(beat: float, bpm: float, beat_one_at_zero: bool = True) -> float:
    if beat_one_at_zero:
        return (beat - 1) * 60 / bpm
    return beat * 60 / bpm

#retrieve notes from chart at difficulty as a list of size 3 dictionaries: {beat, length, hitTime}
def getChartNotes(name: str, difficulty: str = "easy") -> list[ChartNote] | bool:
    
    data = getChartData(name)
    if isinstance(data, bool):
        return False

    #converts the beat value in file to a start time in seconds
    if difficulty in data["charts"]:
        beatChart = data["charts"][difficulty]
        bpm = data["bpm"]
        secondChart: list[ChartNote] = []

        for note in beatChart:
            note["hitTime"] = beatToSeconds(note["beat"], bpm)
            secondChart.append(note)

        return secondChart
    else:
        return False