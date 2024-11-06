import os
import subprocess
import json
import zipfile

# Define the plugins folder and output JSON file path
plugins_folder = "./plugins"
output_json_file = "matches.json"

def extract_zip_files():
    # Check if plugins folder exists
    if not os.path.exists(plugins_folder):
        print("[*]plugins 폴더가 존재하지 않습니다.")
        return
    
    # Loop through files in the plugins folder
    for file_name in os.listdir(plugins_folder):
        if file_name.endswith(".zip"):
            zip_path = os.path.join(plugins_folder, file_name)
            extract_folder = os.path.join(plugins_folder, file_name.replace(".zip", ""))
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
                print(f"[*]{file_name} 압축을 {extract_folder}에 해제했습니다.")

def save_xss_results():
    temp = 'xss_module.py'
    # Run xss_module.py and capture its output
    result = subprocess.run(['python3', temp], capture_output=True, text=True)
    
    # Load JSON data from the output of xss_module.py
    try:
        xss_results = json.loads(result.stdout)
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(xss_results, f, ensure_ascii=False, indent=4)
        print(f"[*]정규표현식 검색 결과가 {output_json_file}에 저장되었습니다.")
    except json.JSONDecodeError:
        print("[*]xss_module.py에서 유효한 JSON 데이터를 받지 못했습니다.")

if __name__ == "__main__":
    extract_zip_files()
    save_xss_results()
