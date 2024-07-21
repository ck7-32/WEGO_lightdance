import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict)):
            return obj
        return json.JSONEncoder.default(self, obj)

def custom_indent(obj, level=0, array_threshold=20):
    if isinstance(obj, dict):
        result = "{\n"
        for key, value in obj.items():
            result += "  " * (level + 1) + json.dumps(key, ensure_ascii=False) + ": "
            result += custom_indent(value, level + 1, array_threshold) + ",\n"
        result = result.rstrip(",\n") + "\n" + "  " * level + "}"
    elif isinstance(obj, list):
        if len(obj) > array_threshold or any(isinstance(item, (list, dict)) for item in obj):
            # 長陣列或包含複雜元素的陣列
            result = "[\n"
            for item in obj:
                result += "  " * (level + 1) + custom_indent(item, level + 1, array_threshold) + ",\n"
            result = result.rstrip(",\n") + "\n" + "  " * level + "]"
        else:
            # 短陣列且只包含簡單元素
            result = json.dumps(obj, cls=CustomJSONEncoder, ensure_ascii=False)
    else:
        result = json.dumps(obj, cls=CustomJSONEncoder, ensure_ascii=False)
    return result

# 讀取 JSON 檔案
file_path = 'data.json'  # 替換成你的 JSON 檔案路徑
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 美化 JSON 並覆寫原檔案
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(custom_indent(data))

print(f"檔案 {file_path} 已成功美化並覆寫。")