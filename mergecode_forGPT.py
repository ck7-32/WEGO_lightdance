import os

def merge_selected_files(file_list, output_file):
    # 取得此腳本所在的資料夾路徑
    folder_path = os.path.dirname(os.path.abspath(__file__))
    
    # 允許的檔案副檔名
    allowed_extensions = ['.py', '.json', '.html', '.js']
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_name in file_list:
            file_ext = os.path.splitext(file_name)[1]
            
            # 確認檔案副檔名是否符合允許的格式
            if file_ext in allowed_extensions:
                file_path = os.path.join(folder_path, file_name)
                
                # 確認檔案是否存在於資料夾中
                if os.path.exists(file_path):
                    # 讀取檔案內容
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                    
                    # 寫入標題和內容到輸出文件
                    outfile.write(f"File: {file_name}\n")
                    outfile.write(f"Extension: {file_ext}\n")
                    outfile.write("Content:\n")
                    outfile.write(content)
                    outfile.write("\n" + "="*40 + "\n\n")
                else:
                    print(f"File not found: {file_name}")
                    
    print(f"Selected files have been merged into {output_file}")

# 使用範例：指定要合併的檔案名稱清單
file_list = ['editor.py', 'index.html', 'main.js', 'setting.json','dancer.js',"translate.py","data.json"]
output_file = "merged_selected_output.txt"
merge_selected_files(file_list, output_file)
