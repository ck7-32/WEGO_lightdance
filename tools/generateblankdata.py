import json
import os
print(os.getcwd())
setting_jsonpath="data\setting.json"
data_jsonpath="data\data.json"
pos_jsonpath="data\pos.json"
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
pos={
        
  "pos": [[]],
  "postimes": [0]
}

with open(setting_jsonpath, 'r', encoding='utf-8') as file:
        setting = json.load(file)

for i in range(len(setting["dancersname"])):
    #data.json相關
        data["frames"].append([])
        data["frames"][i].append([])
        print(setting["dancersname"][i])
        for j in range(len(setting["dancers"][setting["dancersname"][i]]["parts"])):
            data["frames"][i][0].append(0)
    #pos初始化相關
        pos["pos"][0].append([0,0])
        pos["pos"][0][i][0]=100+i*68
        pos["pos"][0][i][1]=50
with open(data_jsonpath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
with open(pos_jsonpath, 'w', encoding='utf-8') as file:
            json.dump(pos, file, ensure_ascii=False)