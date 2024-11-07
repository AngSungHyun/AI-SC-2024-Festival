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
    # result = subprocess.run(['pipenv', 'run', 'python3', temp], capture_output=True, text=True)
    result = subprocess.run(['python3', temp], capture_output=True, text=True)
    
    # Load JSON data from the output of xss_module.py
    try:
        xss_results = json.loads(result.stdout)
        return xss_results
    except json.JSONDecodeError:
        print(f"[*]{temp}에서 유효한 JSON 데이터를 받지 못했습니다.")
        return []

def save_sqli_results():
    temp = 'sqli_module.py'
    # Run sqli_module.py and capture its output
    # result = subprocess.run(['pipenv', 'run', 'python3', temp], capture_output=True, text=True)
    result = subprocess.run(['python3', temp], capture_output=True, text=True)
    
    # Load JSON data from the output of sqli_module.py
    try:
        sqli_results = json.loads(result.stdout)
        return sqli_results
    except json.JSONDecodeError:
        print(f"[*]{temp}에서 유효한 JSON 데이터를 받지 못했습니다.")
        return []

if __name__ == "__main__":
    extract_zip_files()
    xss_results = save_xss_results()
    sqli_results = save_sqli_results()
    
    # Combine results into a single list
    combined_results = xss_results + sqli_results
    
    # Save combined results to JSON file
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, ensure_ascii=False, indent=4)
    print(f"[*]XSS 및 SQLi 검색 결과가 {output_json_file}에 저장되었습니다.")