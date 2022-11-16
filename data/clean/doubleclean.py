import json

with open('data/clean/stations.json', encoding='utf-8') as file:
    file_contents = file.read()

cleaned = json.loads(file_contents)

with open('data/clean/stationsNew.json', encoding='utf-8') as file:
    time_contents = file.read()

new = json.loads(time_contents)

for i in cleaned:
	for vi in i['connections']:
		for j in new:
			for vj in j['connections']:
				if i["id"]==j["id"] and vi['id'] == vj['id']:
					vj['expectTakeTime'] = vi['cost'] - vj['cost']

print(new)

with open('data/clean/station-1.json', 'w') as f:
    json.dump(new, f, indent=4)