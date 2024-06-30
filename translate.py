import json
import os

# 讀取原始JSON檔案
with open('data.json', 'r',encoding="utf-8") as f:
    data = json.load(f)

frames = data.get("frames", [])

# 建立輸出資料夾
output_dir = 'output_jsons'
os.makedirs(output_dir, exist_ok=True)
# 分割並儲存每個frame的parts
out={"frame":[],"define":""}
for i in range(3):
    out={"frame":[]}
    for j in range(len(frames[i])):
        out["frame"].append([])
        for y in range(len(frames[i][j])):
            out["frame"][j].append(frames[i][j][y])
    a=len(out["frame"])
    b=len(out["frame"][0])
    out["define"]=f"[{a}][{b}]"
    output_file = os.path.join(output_dir, f'frame_{i}.json')
    text_file=os.path.join(output_dir, f'frame_{i}.txt')
    c=out["frame"]
    text=f"int data[{a}][{b}] = {c}"
    with open(output_file, 'w') as f:
        json.dump(out, f, sort_keys=True)
    with open(text_file, 'w') as f:
        f.write(text)