result=[]
up="[0,0,0,0,0,0,0,4,4,4,4]"
down="[1,6,2,1,1,1,1,0,0,0,0]"
alllightup="[1,6,2,1,1,1,1,4,4,4,4]"
alloff="[0,0,0,0,0,0,0,0,0,0,0]"
slowsparkle=30
slowsparkletimes=6
def add_milliseconds(input_time, additional_milliseconds):
    # 將輸入的時間字串轉換為秒數
    input_time_list = input_time.split('.')
    minutes, seconds, milliseconds = map(int, input_time_list)
    total_seconds = minutes * 60 + seconds + milliseconds / 1000.0

    # 加上額外的毫秒數
    total_seconds += additional_milliseconds / 1000.0

    # 計算新的分鐘、秒、毫秒
    new_minutes = int(total_seconds // 60)
    new_seconds = int(total_seconds % 60)
    new_milliseconds = int((total_seconds % 1) * 1000)

    # 格式化輸出字串，確保位數一致
    result_time = f"{new_minutes:02d}.{new_seconds:02d}.{new_milliseconds:03d}"

    return result_time

def shineA(time):
    return(f"{time}\t{up} {down} {up} {down} {up}\n")
def shineB(time):
    return(f"{time}\t{down} {up} {down} {up} {down}\n")
def shineC(time):
    return(f"{time}\t{alllightup} {alloff} {alllightup} {alloff} {alllightup}\n")
def shineD(time):
    return(f"{time}\t{alloff} {alllightup} {alloff} {alllightup} {alloff}\n")
def process_text(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
             result.append(line)
            
            for line in range(len(result)):
                if result[line]=="閃1\n":
                    gettime=result[line+1].split("\t")[0]
                    slowsparkle=int(result[line+1].split("\t")[1].split()[0])
                    slowsparkletimes=int(result[line+1].split("\t")[1].split()[1])
                    print(slowsparkle)
                    result[line+1]=""
                    result[line]=shineA(gettime)
                    for i in range(slowsparkletimes-1):
                        if i%2==0:
                            result.insert(line+2,shineB(add_milliseconds(gettime,slowsparkle*(slowsparkletimes-i-1))))   
                        else:
                            result.insert(line+2,shineA(add_milliseconds(gettime,slowsparkle*(slowsparkletimes-i-1)))) 
                if result[line]=="閃2\n":
                    gettime=result[line+1].split("\t")[0]
                    slowsparkle=int(result[line+1].split("\t")[1].split()[0])
                    slowsparkletimes=int(result[line+1].split("\t")[1].split()[1])
                    print(slowsparkle)
                    result[line+1]=""
                    result[line]=shineC(gettime)
                    for i in range(slowsparkletimes-1):
                        if i%2==0:
                            result.insert(line+2,shineD(add_milliseconds(gettime,slowsparkle*(slowsparkletimes-i-1))))   
                        else:
                            result.insert(line+2,shineC(add_milliseconds(gettime,slowsparkle*(slowsparkletimes-i-1)))) 
            for line in range(len(result)):
                # 檢查每一行是否包含 "，" 並處理空格
                if ', ' in result[line]:
                    result[line] = result[line].replace(', ', ',')
                outfile.write(result[line])
        print("處理完成，輸出到", output_file)
    except Exception as e:
        print("發生錯誤:", str(e))

# 使用範例
input_filename = "LED_light_dance_clothes.in"  # 輸入檔案名稱
output_filename = "output.txt"  # 輸出檔案名稱

process_text(input_filename, output_filename)
