import json

DANCER = 3
PART = 9
Dancers = []
time_lst = []
dancer_lst = []
now_lst = []
lst_token = []
Time = []

for i in range(DANCER):
    Dancers.append([])
    Time.append([])
    dancer_lst.append([])
    now_lst.append([0 for j in range(PART)])

# 打開文件
with open("output.txt", encoding='utf-8') as lst, open("light.txt", "w") as Js, open("data.js", 'w') as pos:
    for line in lst:
        if line[0] == "#" or line[0].strip() == "":  # 如果???# 或一整行空就??
            continue
        else:
            arr_lst = []
            token = line.split()
            # 轉成毫秒
            Min, Sec, Mil_sec = map(float, token[0].split("."))
            time = str(int(((Min * 60 + Sec) * 1000) + Mil_sec))
            time_lst.append(int(time))
            for i in range(1, DANCER + 1):
                arr_lst.append(list(map(int, eval(token[i]))))
            for i in range(DANCER):
                if arr_lst[i] == []:
                    arr_lst[i] = now_lst[i]
                dancer_lst[i].append(arr_lst[i])
            now_lst = arr_lst
            for i in range(1, DANCER + 1):
                #刪除重複的
                if lst_token != []:
                    if lst_token[i] == token[i]:
                        token[i] = "[]"
                token[i] = eval(token[i])
                if token[i] != []:
                    #刪除多餘的(特殊)
                    token[i].pop(5)
                    token[i].pop(5)
                    token[i].pop(6)
                    token[i].pop(6)
                    token[i].pop(6)
                    token[i].pop(3)
                    token[i] = "{" + ",".join(map(str, token[i])) + "}"
                    Dancers[i - 1].append(token[i])
                    Time[i - 1].append(time)
            lst_token = line.split()
            print("===========================")

    # 導入 light.txt
    for dancer_data in range(len(Dancers)):
        Js.write("Pos : ")
        Js.write(str(len(Dancers[dancer_data])))
        Js.write("{")
        Js.write(", ".join(map(str, Dancers[dancer_data])))
        Js.write("}\n")
        Js.write("Time : ")
        Js.write(str(len(Time[dancer_data])))
        Js.write("{")
        Js.write(", ".join(map(str, Time[dancer_data])))
        Js.write("}\n")

    # 導入 data.js
    pos.write("var Data = \"")
    pos.write(json.dumps(time_lst))
    pos.write("\";")
    pos.write("\nvar light = \"")
    pos.write(json.dumps(dancer_lst))
    pos.write("\";")
