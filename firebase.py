import os
import json
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK with config
import os
config_path = os.path.join(os.path.dirname(__file__), 'firebase_config.json')
with open(config_path, 'r', encoding='utf-8') as config_file:
    firebase_config = json.load(config_file)

cred = credentials.Certificate(firebase_config['credentialPath'])
firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_config['databaseURL']
})

import hashlib

def get_object_depth(obj, current=0):
    """遞迴計算物件深度"""
    if not isinstance(obj, (dict, list)):
        return current
    if isinstance(obj, dict):
        return max((get_object_depth(v, current+1) for v in obj.values()), default=current)
    return max((get_object_depth(v, current+1) for v in obj), default=current)

def get_file_hash(filepath):
    """Calculate SHA-256 hash of a file"""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

from threading import Timer

sync_timer = None
is_syncing = False

def original_update_firebase_from_json(data_dir, firebase_base_path, max_retries):
    global is_syncing
    is_syncing = True
    try:
        hash_store_path = os.path.join(os.path.dirname(__file__), firebase_config['syncSettings']['hashStore'])
        
        # Load existing hashes
        try:
            with open(hash_store_path, 'r', encoding='utf-8') as f:
                hashes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            hashes = {}

        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                json_path = os.path.join(data_dir, filename)
                firebase_path = f"{firebase_base_path}/{filename[:-5]}"
                
                # Calculate current hash
                current_hash = get_file_hash(json_path)
                
                # Check if file has changed
                if hashes.get(json_path) == current_hash:
                    continue
                    
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        with open(json_path, 'r', encoding='utf-8') as json_file:
                            data = json.load(json_file)
                        ref = db.reference(firebase_path)
                        ref.set(data)
                        # Update hash store on success
                        hashes[json_path] = current_hash
                        with open(hash_store_path, 'w', encoding='utf-8') as f:
                            json.dump(hashes, f)
                        break
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            raise RuntimeError(f"Failed to update {filename} after {max_retries} attempts: {str(e)}")
    finally:
        is_syncing = False

def update_firebase_from_json(data_dir, firebase_base_path, max_retries=3):
    global sync_timer
    
    def sync_task():
        if not is_syncing:
            original_update_firebase_from_json(data_dir, firebase_base_path, max_retries)
    
    if sync_timer:
        sync_timer.cancel()
        
    sync_timer = Timer(
        firebase_config['syncSettings']['debounceTime'] / 1000, 
        sync_task
    )
    sync_timer.start()

def update_json_from_firebase(data_dir, firebase_base_path, max_retries=3):
    ref = db.reference(firebase_base_path)
    data = ref.get()
    
    for key, value in data.items():
            # 過濾無效key值
            if not key or not isinstance(key, str) or len(key) > 100:
                print(f"忽略無效Firebase鍵值: {repr(key)}")
                continue
            
            # 安全檔名處理
            safe_key = key.replace('/', '_').replace('..', '').strip().strip('.')
            if not safe_key:
                print(f"轉換後空白的鍵值: {repr(key)}")
                continue
                
            json_path = os.path.join(data_dir, f"{safe_key}.json")
            
            # 檢查資料大小
            data_size = len(json.dumps(value))
            if data_size > 1024*1024:  # 1MB限制
                print(f"拒絕過大資料 {safe_key}.json ({data_size//1024}KB)")
                continue
                
            retry_count = 0
            while retry_count < max_retries:
                try:
                    with open(json_path, 'w', encoding='utf-8') as json_file:
                        json.dump(value, json_file, indent=4)
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        raise RuntimeError(f"Failed to save {safe_key}.json after {max_retries} attempts: {str(e)}")

def listen_to_firebase_and_update_json(data_dir, firebase_base_path):
    ref = db.reference(firebase_base_path)
    
    def listener(event):
        try:
            # 安全路徑處理
            relative_path = event.path.lstrip('/')  # 移除開頭斜線
            # 處理空路徑並限制資料大小
            base_name = relative_path.replace('/', '_').replace('..', '').strip().strip('.')[:100]
            if not base_name:
                base_name = 'default_data'
            
            # 強制加入時間戳記並驗證檔名
            import time
            timestamp = int(time.time())
            base_part = os.path.splitext(base_name)[0] or f"unnamed_{timestamp}"
            safe_filename = f"{base_part}_{timestamp}.json"
            file_path = os.path.join(data_dir, safe_filename)
            
            # 檢查資料大小並限制最大為1MB
            data_size = len(json.dumps(event.data))
            if data_size > 1024*1024:
                print(f"警告：拒絕寫入過大檔案 {safe_filename} (大小: {data_size//1024}KB)")
                print(f"資料來源路徑: {event.path}")
                print(f"資料類型: {type(event.data)}")
                print(f"資料結構深度: {get_object_depth(event.data)}")
                return
            
            # 檢查是否為有效JSON結構
            try:
                json.loads(json.dumps(event.data))
            except Exception as e:
                print(f"無效JSON資料: {str(e)}")
                return
            os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 建立完整目錄結構
            
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(event.data, json_file, indent=4)
        except Exception as e:
            print(f"Firebase監聽寫入失敗: {str(e)}")
    
    ref.listen(listener)

# Example usage:
# update_firebase_from_json('path/to/your/local.json', 'path/in/firebase')
# update_json_from_firebase('path/to/your/local.json', 'path/in/firebase')
# listen_to_firebase_and_update_json('path/to/your/local.json', 'path/in/firebase')
