import glob
import json
files = glob.glob("dados/celebs/*.json")
for filename in files:
    with open(filename, 'r', encoding="utf8") as f:
        print(filename)
        data = json.load(f)

        for item in data:
            replie_to = data[item]['replie_to']
            if(replie_to is not None):
                data[item]['response_time'] = data[item]['created_at'] / \
                    1000 - data[replie_to]['created_at']/1000
            else:
                data[item]['response_time'] = 0.0
    with open(filename, 'w', encoding="utf8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
