import os
import re
import json

plugins_folder = "./plugins"

sql_patterns = [
    r'mysqli?_query\s*\(\s*[^,]*\$[^,]+\)',  # mysqli_query($conn, $query) 형태
    r'(\$.*?)->query\s*\(\s*[^,]*\$[^,]+\)',  # $pdo->query($query) 형태
    r'execute\s*\(\s*[^,]*\$[^,]+\)',         # prepare()->execute($params) 형태
    r'SELECT.*?FROM.*?WHERE.*?\$',            # SELECT ... WHERE 절에 변수 사용
    r'INSERT.*?INTO.*?VALUES.*?\$',           # INSERT INTO ... VALUES 에 변수 사용
    r'UPDATE.*?SET.*?\$',                     # UPDATE ... SET 에 변수 사용
    r'DELETE.*?FROM.*?WHERE.*?\$'             # DELETE FROM ... WHERE 에 변수 사용
]

def search_for_pattern():
    results = []

    for root, _, files in os.walk(plugins_folder):
        for extracted_file in files:
            if extracted_file.endswith(".php"):
                file_path = os.path.join(root, extracted_file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        for pattern in sql_patterns:
                            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                            for match in matches:
                                matched_text = match.group().strip()
                                # 줄바꿈이 포함된 경우 첫 번째 줄만 사용
                                matched_text = matched_text.split('\n')[0].strip()

                                results.append({
                                    "file_path": file_path,
                                    "match": matched_text
                                })

                except OSError as e:
                    print(f"파일 읽기 오류 {file_path}: {str(e)}")

    # 결과 출력
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    search_for_pattern()
