from charts import *
import json
import random

notes: list[ChartNote] = []

for i in range(200):
    n: ChartNote = {
        "beat" : 10 + (i / 2) + random.randint(-3,3) / 2,
        "length" : 0,
        "lane" : random.randint(0,3)
    }
    notes.append(n)

data: ChartFile = {
    "name" : "test",
    "bpm" : 120,
    "charts" : {
        "easy" : notes
    }
}

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
