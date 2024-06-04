import json
import re

# 常量設定
DANCER = 3
PART = 9

# 處理文本數據
def process_text(input_file, output_file):
    result = []
    up = "[6,7,2,6,6,6,6,0,0,0,0]"
    down = "[0,0,0,0,0,0,0,5,5,5,5]"
    upB = "[7,7,7,7,7,7,7,5,5,5,5]"
    downB = "[5,5,5,5,5,5,5,7,7,7,7]"
    alllightup = "[6,7,2,6,6,6,6,5,5,5,5]"
    alloff = "[0,0,0,0,0,0,0,0,0,0,0]"
    allred = "[1,1,1,1,1,1,1,1,1,1,1]"
    allwhite = "[7,7,7,7,7,7,7,7,7,7,7]"
    allblue = "[5,5,5,5,5,5,5,5,5,5,5]"
    allpurple = "[6,6,6,6,6,6,6,6,6,6,6]"
    allorange = "[3,3,3,3,3,3,3,3,3,3,3]"

    def add_milliseconds(input_time, additional_milliseconds):
        input_time_list = input_time.split('.')
        minutes, seconds, milliseconds = map(int, input_time_list)
        total_seconds = minutes * 60 + seconds + milliseconds / 1000.0
        total_seconds += additional_milliseconds / 1000.0
        new_minutes = int(total_seconds // 60)
        new_seconds = int(total_seconds % 60)
        new_milliseconds = int((total_seconds % 1) * 1000)
        return f"{new_minutes:02d}.{new_seconds:02d}.{new_milliseconds:03d}"

    def shineA(time): return f"{time}\t{upB} {downB} {upB}\n"
    def shineB(time): return f"{time}\t{downB} {upB} {downB}\n"
    def shineC(time): return f"{time}\t{alllightup} {alloff} {alllightup}\n"
    def shineD(time): return f"{time}\t{alloff} {alllightup} {alloff}\n"
    def shineE(time): return f"{time}\t{allorange} {allred} {allorange}\n"
    def shineF(time): return f"{time}\t{allred} {allorange} {allred}\n"
    def shineH(time): return f"{time}\t{allred} {allred} {allred}\n"
    def shineG(time): return f"{time}\t{alloff} {alloff} {alloff}\n"
    def shineI(time): return f"{time}\t{allwhite} {allblue} {allwhite}\n"
    def shineW(time): return f"{time}\t{allblue} {allwhite} {allblue}\n"
    def shineP(time): return f"{time}\t{allpurple} {allpurple} {allpurple}\n"
    def shineU(time): return f"{time}\t{up} {down} {up}\n"
    def shineY(time): return f"{time}\t{down} {up} {down}\n"

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                result.append(line)
            line = len(result) - 1
            while line >= 0:
                if result[line] == "閃1\n":
                    gettime = result[line + 1].split("\t")[0]
                    slowsparkle = int(result[line + 1].split("\t")[1].split()[0])
                    slowsparkletimes = int(result[line + 1].split("\t")[1].split()[1])
                    result[line + 1] = ""
                    result[line] = shineA(gettime)
                    for i in range(slowsparkletimes - 1):
                        if i % 2 == 0:
                            result.insert(line + 2, shineB(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))   
                        else:
                            result.insert(line + 2, shineA(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))
                elif result[line] == "閃2\n":
                    gettime = result[line + 1].split("\t")[0]
                    slowsparkle = int(result[line + 1].split("\t")[1].split()[0])
                    slowsparkletimes = int(result[line + 1].split("\t")[1].split()[1])
                    result[line + 1] = ""
                    result[line] = shineC(gettime)
                    for i in range(slowsparkletimes - 1):
                        if i % 2 == 0:
                            result.insert(line + 2, shineD(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))   
                        else:
                            result.insert(line + 2, shineC(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))
                elif result[line] == "閃0\n":
                    gettime = result[line + 1].split("\t")[0]
                    slowsparkle = int(result[line + 1].split("\t")[1].split()[0])
                    slowsparkletimes = int(result[line + 1].split("\t")[1].split()[1])
                    result[line + 1] = ""
                    result[line] = shineE(gettime)
                    for i in range(slowsparkletimes - 1):
                        if i % 2 == 0:
                            result.insert(line + 2, shineF(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))   
                        else:
                            result.insert(line + 2, shineE(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))
                elif result[line] == "閃3\n":
                    gettime = result[line + 1].split("\t")[0]
                    slowsparkle = int(result[line + 1].split("\t")[1].split()[0])
                    slowsparkletimes = int(result[line + 1].split("\t")[1].split()[1])
                    result[line + 1] = ""
                    result[line] = shineG(gettime)
                    for i in range(slowsparkletimes - 1):
                        if i % 2 == 0:
                            result.insert(line + 2, shineH(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))   
                        else:
                            result.insert(line + 2, shineG(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))
                elif result[line] == "閃4\n":
                    gettime = result[line + 1].split("\t")[0]
                    slowsparkle = int(result[line + 1].split("\t")[1].split()[0])
                    slowsparkletimes = int(result[line + 1].split("\t")[1].split()[1])
                    result[line + 1] = ""
                    result[line] = shineI(gettime)
                    for i in range(slowsparkletimes - 1):
                        if i % 2 == 0:
                            result.insert(line + 2, shineW(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))   
                        else:
                            result.insert(line + 2, shineI(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))
                elif result[line] == "閃5\n":
                    gettime = result[line + 1].split("\t")[0]
                    slowsparkle = int(result[line + 1].split("\t")[1].split()[0])
                    slowsparkletimes = int(result[line + 1].split("\t")[1].split()[1])
                    result[line + 1] = ""
                    result[line] = shineP(gettime)
                    for i in range(slowsparkletimes - 1):
                        if i % 2 == 0:
                            result.insert(line + 2, shineG(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))   
                        else:
                            result.insert(line + 2, shineP(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))
                elif result[line] == "閃6\n":
                    gettime = result[line + 1].split("\t")[0]
                    slowsparkle = int(result[line + 1].split("\t")[1].split()[0])
                    slowsparkletimes = int(result[line + 1].split("\t")[1].split()[1])
                    result[line + 1] = ""
                    result[line] = shineU(gettime)
                    for i in range(slowsparkletimes - 1):
                        if i % 2 == 0:
                            result.insert(line + 2, shineY(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))   
                        else:
                            result.insert(line + 2, shineU(add_milliseconds(gettime, slowsparkle * (slowsparkletimes - i - 1))))
                line -= 1

            # 儲存結果到輸出文件
            for line in result:
                if line:
                    outfile.write(line)

    except Exception as e:
        print(f"An error occurred: {e}")

# 處理 JSON 數據
def process_json(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
        
        # 移除重複的燈光效果
        unique_effects = {}
        output_data = []

        for entry in data:
            effect = entry["light_effect"]
            if effect not in unique_effects:
                unique_effects[effect] = len(unique_effects)
            output_data.append({
                "time": entry["time"],
                "light_effect": unique_effects[effect]
            })
        
        # 儲存優化後的 JSON 數據
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump({"unique_effects": list(unique_effects.keys()), "data": output_data}, outfile, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")

# 主函數
if __name__ == "__main__":
    text_input_file = "LED_light_dance_clothes.in"
    text_output_file = "output.txt"
    json_input_file = "input.json"
    json_output_file = "output.json"

    process_text(text_input_file, text_output_file)
    process_json(json_input_file, json_output_file)
