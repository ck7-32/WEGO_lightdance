import json
setting_jsonpath="setting.json"
data_jsonpath="data.json"

data={"color": [
        "#000000"
    ],
    "colornames": [
        "黑"
    ],
    "frames": [

    ],
    "frametimes": [
        0
        ]}
with open(setting_jsonpath, 'r', encoding='utf-8') as file:
        setting = json.load(file)

for i in range(len(setting["dancersname"])):
        data["frames"].append([])
        data["frames"][i].append([])
        print(setting["dancersname"][i])
        for j in range(len(setting["dancers"][setting["dancersname"][i]]["parts"])):
            
            data["frames"][i][0].append(0)
with open(data_jsonpath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)