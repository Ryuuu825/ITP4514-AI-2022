import json

with open('data/dirty/heuristic.json', encoding='utf-8') as file:
    file_contents = file.read()

data = json.loads(file_contents)

h = dict()
for key, value in data.items():
		d= dict()
		d[key] = 0
		for i in value:
			d[str(i[0])] = i[1]
		if key != '39':
			d['44'] = d['39']
		if key != '40':
			d['45'] = d['40']
		if key != '42':
			d['46'] = d['42']
		h[key] = d
h['44'] = h['39']
h['45'] = h['40']
h['46'] = h['42']
with open('data/clean/nodes_heuristic.json', 'w') as f:
    json.dump(h, f, indent=4)