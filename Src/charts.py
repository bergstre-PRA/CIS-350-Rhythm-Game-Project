from pathlib import Path
import json

ASSETS_DIR = Path(__file__).parent.parent / "Assets"
SONGS_DIR = ASSETS_DIR / "Songs"
CHARTS_DIR = ASSETS_DIR / "Chart Files"

_savedData = {}

#checks if the song mp3 exists and returns it
def find_song(name):
    for file in SONGS_DIR.iterdir():
        if file.is_file() and file.name == str(name) + ".mp3":
            return file
    return False

#checks if chart file exists and returns it
def getChartFile(name):
    for file in CHARTS_DIR.iterdir():
            if file.is_file() and file.name == str(name) + ".json":
                return file
    return False

#retrieves data from chart json, caches already loaded data
def getChartData(name):
    if name in _savedData:
        return _savedData[name]

    chart = getChartFile(name)
    if chart == False:
        return False
    with open(chart, "r") as file:
        data = json.load(file)
    _savedData[name] = data
    return data

#retrieve song name from chart
def getSongName(name):
    data = getChartData(name)
    if data == False:
        return False
    
    return data["name"]

#retrieve song bpm from chart
def getBpm(name):
    data = getChartData(name)
    if data == False:
        return False
    
    return data["bpm"]

#Converts a beat number to a timestamp in seconds.
#beat_one_at_zero=True: Beat 1 occurs at 0.0 seconds.
def beatToSeconds(beat, bpm, beat_one_at_zero=True):
    if beat_one_at_zero:
        return (beat - 1) * 60 / bpm
    return beat * 60 / bpm

#retrieve notes from chart at difficulty as a list of size 3 dictionaries: {beat, length, hitTime}
def getChartNotes(name, difficulty="easy"):
    
    data = getChartData(name)
    if data == False:
        return False

    #converts the beat value in file to a start time in seconds
    if difficulty in data["charts"]:
        beatChart = data["charts"][difficulty]
        bpm = data["bpm"]
        secondChart = []
        for n in beatChart:
            note = n
            note["hitTime"] = beatToSeconds(n["beat"], bpm)
            secondChart.append(note)
        return secondChart
    else:
        return False

chart = getChartNotes("SRGS1")
for n in chart:
    print(n)