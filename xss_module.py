import os
import re
import json

plugins_folder = "./plugins"
output_pattern = r'<input [^>]*value=[\'"]\''

def search_for_pattern():
    results = [] 

    for root, _, files in os.walk(plugins_folder):
        for extracted_file in files:

            if extracted_file.endswith(".php") or extracted_file.endswith(".html"):
                file_path = os.path.join(root, extracted_file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    output_matches = re.findall(output_pattern, content)
                    
                    for match in output_matches:
                        results.append({"file_path": file_path, "match": match})

    print(json.dumps(results))

if __name__ == "__main__":
    search_for_pattern()