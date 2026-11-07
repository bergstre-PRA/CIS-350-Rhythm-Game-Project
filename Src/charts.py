"""Helpers for locating songs and reading chart data."""

import json
from pathlib import Path
from typing import NotRequired, TypeAlias, TypedDict

ASSETS_DIR = Path(__file__).parent.parent / "Assets"
SONGS_DIR = ASSETS_DIR / "Songs"
CHARTS_DIR = ASSETS_DIR / "Chart Files"


class ChartNote(TypedDict):
    """Data for a single note in a chart."""

    beat: float
    length: float
    lane: int
    hit_time: NotRequired[float]


class ChartFile(TypedDict):
    """Dictionary structure for a chart JSON."""

    name: str
    bpm: float
    charts: dict[str, list[ChartNote]]


Charts: TypeAlias = dict[str, ChartFile | None]


_cached_charts: Charts = {}


def find_song(name: str) -> Path | None:
    """Return the song file for a given track name."""
    for file in SONGS_DIR.iterdir():
        if file.is_file() and file.name == str(name) + ".mp3":
            return file
    return None


def get_chart_file(name: str) -> Path | None:
    """Return the chart file for a given song name."""
    for file in CHARTS_DIR.iterdir():
        if file.is_file() and file.name == str(name) + ".json":
            return file
    return None


def get_chart_data(name: str) -> ChartFile | None:
    """Read and cache a chart file for a song."""
    if name in _cached_charts:
        return _cached_charts[name]

    chart = get_chart_file(name)
    if chart is None:
        return None

    with open(chart, "r", encoding="utf-8") as file:
        data = json.load(file)
    _cached_charts[name] = data
    return data


def get_song_name(name: str) -> str | None:
    """Return the display name of a song if it exists."""
    data = get_chart_data(name)
    if data is None:
        return None
    return data["name"]


def get_bpm(name: str) -> float | None:
    """Return the BPM for a song from its name."""
    data = get_chart_data(name)
    if data is None:
        return None
    return data["bpm"]


def beat_to_seconds(beat: float, bpm: float, start_one: bool = True) -> float:
    """Convert a beat position to seconds."""
    if start_one:
        return (beat - 1) * 60 / bpm
    return beat * 60 / bpm


def get_chart_notes(
    name: str,
    difficulty: str = "easy",
) -> list[ChartNote] | None:
    """Return the chart notes for the selected difficulty."""
    data = get_chart_data(name)
    if data is None:
        return None

    if difficulty in data["charts"]:
        beat_chart = data["charts"][difficulty]
        bpm = data["bpm"]
        second_chart: list[ChartNote] = []

        for note in beat_chart:
            hit_time = note.get("hit_time", note.get("hitTime"))
            if hit_time is None:
                note["hit_time"] = beat_to_seconds(note["beat"], bpm)
            else:
                note["hit_time"] = hit_time
            second_chart.append(note)

        return second_chart
    return None
