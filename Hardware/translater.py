import json
import os
def replace_brackets(input_string):
    # 將所有 [ 換成 {
    input_string = input_string.replace('[', '{')
    # 將所有 ] 換成 }
    input_string = input_string.replace(']', '}')
    return input_string
# 讀取原始JSON檔案
with open('data.json', 'r',encoding="utf-8") as f:
    data = json.load(f)

frames = data.get("frames", [])

# 建立輸出資料夾
output_dir = 'output_jsons'
os.makedirs(output_dir, exist_ok=True)
# 分割並儲存每個frame的parts
out={"frame":[],"define":""}
for dancerN in range(3):
    out={"frame":[]}
    for frameN in range(len(frames[dancerN])):
        out["frame"].append([])
        for partN in range(len(frames[dancerN][frameN])):
            out["frame"][frameN].append(frames[dancerN][frameN][partN])
    a=len(out["frame"])
    b=len(out["frame"][0])
    out["define"]=f"[{a}][{b}]"
    output_file = os.path.join(output_dir, f'frame_{dancerN}.json')
    text_file=os.path.join(output_dir, f'frame_{dancerN}.txt')
    c=out["frame"]
    text=f"{c};"
    ot=replace_brackets(text)
    ott=f"int data[{a}][{b}] = {ot}"
    #with open(output_file, 'w') as f:
    #json.dump(out, f, sort_keys=True)
    with open(text_file, 'w') as f:
        f.write(oot)