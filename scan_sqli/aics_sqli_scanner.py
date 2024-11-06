import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from colorama import init, Fore, Style
import os
import json

if os.name == 'nt':  # Windows
    os.system('cls')
else:  # Mac OS, Linux
    os.system('clear')
    
init()  # colorama init

queries = []
base_queries = []
forms = []
findings = [] # result save

# url parse 
# url = "http://127.0.0.1:5012/login"
url = "https://redtiger.labs.overthewire.org/level1.php" # test 사이트

parsed_url = urlparse(url)
base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

print("\n\n======================basic info=================")
print("url: ", url)
print("base_url: ", base_url)

def get_links_from_a_tag(url):
    # Get links from URL and check for endpoints
    re = requests.get(url, verify=False)  # Disable SSL certificate verification
    soup = BeautifulSoup(re.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '?' in href:
            # Extract query parameter part from URL
            query_part = href.split('?')[1]
            # Split query parameters by &
            query_params = query_part.split('&')
            
            if href.startswith('?'):
                # Generate query parameter combinations for URLs starting with ?
                for i in range(len(query_params)):
                    query = '?' + '&'.join(query_params[:i+1])
                    if query not in queries:
                        queries.append(query)
            
            elif href.startswith('/'):
                # Generate query parameter combinations for URLs starting with /
                base_path = href.split('?')[0]
                for i in range(len(query_params)):
                    query = base_path + '?' + '&'.join(query_params[:i+1]) 
                    if query not in base_queries:
                        base_queries.append(query)


def get_forms_from_form_tag(url):
    # Extract forms from URL
    re = requests.get(url, verify=False)
    soup = BeautifulSoup(re.content, 'html.parser')
    for form in soup.find_all('form'):
        action = form.get('action') if form.get('action') is not None else parsed_url.path
        inputs = []
        for input_tag in form.find_all('input'):
            input_name = input_tag.get('name')
            if input_name:
                inputs.append(input_name)
        forms.append({'action': action, 'inputs': inputs})


get_links_from_a_tag(url)
get_forms_from_form_tag(url)

print("queries: ", queries)
print("base_queries: ", base_queries)
print("forms: ", forms)
print("===================================================\n\n")

payloads = open("payloads.txt", "r").read().splitlines()

def scan_a_get(input_url, input_queries):
    for input_query in input_queries:
        # Measure base response time
        start_time = time.time()
        temp_response = requests.get(f"{input_url}{input_query}", verify=False)
        base_time = time.time() - start_time
        print(f"{Fore.YELLOW}[info] Base response time for {input_url}{input_query}: {base_time:.2f} seconds{Style.RESET_ALL}")
        
        # Set threshold (2.5 times the base response time)
        threshold = max(3.0, base_time * 2.5)
        
        for payload in payloads:
            # print("query: ", input_query)
            new_url = f"{input_url}{input_query} {payload}"
            # print("new_url: ", new_url)
            
            # Measure payload execution time
            start_time = time.time()
            re = requests.get(new_url, verify=False)
            elapsed_time = time.time() - start_time
            
            # If response time exceeds threshold, potential vulnerability found
            if elapsed_time > threshold:
                finding = {
                    'type': 'GET',
                    'url': new_url,
                    'payload': payload,
                    'response_time': elapsed_time
                }
                findings.append(finding)
                
                print(f"{Fore.GREEN}[find]{Style.RESET_ALL}")
                print(f"{Fore.GREEN}URL: {new_url}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Payload: {payload}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Response time: {elapsed_time:.2f} seconds{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[done] {new_url} - No issues found{Style.RESET_ALL}")

def scan_form_post(input_url, input_forms):
    for input_form in input_forms:
        # Measure base response time
        datas = {input_name: "test" for input_name in input_form['inputs']}
        # print("datas: ", datas)
        start_time = time.time()
        temp_response = requests.post(f"{input_url}{input_form['action']}", data=datas, verify=False)
        base_time = time.time() - start_time
        print(f"{Fore.YELLOW}[info] Base response time ({input_url}{input_form['action']}): {base_time:.2f} seconds{Style.RESET_ALL}")
        
        # Set threshold (2.5 times the base response time)
        threshold = max(3.0, base_time * 2.5)
        
        for payload in payloads:
            datas = {
                **{input_name: payload for input_name in input_form['inputs']}
            }
            # print("data: ", datas)
            
            # Measure payload execution time
            start_time = time.time()
            re = requests.post(f"{input_url}{input_form['action']}", data=datas, verify=False)
            elapsed_time = time.time() - start_time
            
            # If response time exceeds threshold, potential vulnerability found
            if elapsed_time > threshold:
                finding = {
                    'type': 'POST',
                    'url': f"{input_url}{input_form['action']}",
                    'payload': payload,
                    'response_time': elapsed_time,
                    'data': datas
                }
                findings.append(finding)
                
                print(f"{Fore.GREEN}[found]{Style.RESET_ALL}")
                print(f"{Fore.GREEN}URL: {input_url}{input_form['action']}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Payload: {payload}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Response time: {elapsed_time:.2f} seconds{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[done] {input_url}{input_form['action']} - {datas} - No issues found{Style.RESET_ALL}")

def scan_form_get(input_url, input_forms):
    for input_form in input_forms:
        # Generate query parameters for measuring base response time
        query_params = {input_name: "test" for input_name in input_form['inputs']}
        query_string = "&".join([f"{k}={v}" for k,v in query_params.items()])
        test_url = f"{input_url}{input_form['action']}?{query_string}"
        # print("test_url: ", test_url)
        
        # Measure base response time
        start_time = time.time()
        temp_response = requests.get(test_url, verify=False)
        base_time = time.time() - start_time
        print(f"{Fore.YELLOW}[info] Base response time ({test_url}): {base_time:.2f} seconds{Style.RESET_ALL}")
        
        # Set threshold (2.5 times the base response time)
        threshold = max(3.0, base_time * 2.5)
        
        for payload in payloads:
            # Generate query parameters with payload
            query_params = {input_name: payload for input_name in input_form['inputs']}
            query_string = "&".join([f"{k}={v}" for k,v in query_params.items()])
            test_url = f"{input_url}{input_form['action']}?{query_string}"
            
            # Measure payload execution time
            start_time = time.time()
            re = requests.get(test_url, verify=False)
            elapsed_time = time.time() - start_time
            
            # If response time exceeds threshold, potential vulnerability found
            if elapsed_time > threshold:
                finding = {
                    'type': 'FORM-GET',
                    'url': test_url,
                    'payload': payload,
                    'response_time': elapsed_time
                }
                findings.append(finding)
                
                print(f"{Fore.GREEN}[found]{Style.RESET_ALL}")
                print(f"{Fore.GREEN}URL: {test_url}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Payload: {payload}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Response time: {elapsed_time:.2f} seconds{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[done] {test_url} - No issues found{Style.RESET_ALL}")
        
try:
    if queries:
        scan_a_get(url, queries)
except:
    print(f"{Fore.RED}[error] Error occurred while scanning queries, continuing...{Style.RESET_ALL}")

try:
    if base_queries:
        scan_a_get(base_url, base_queries)
except:
    print(f"{Fore.RED}[error] Error occurred while scanning base_queries, continuing...{Style.RESET_ALL}")

try:
    if forms:
        scan_form_post(base_url, forms)
except:
    print(f"{Fore.RED}[error] Error occurred while scanning forms, continuing...{Style.RESET_ALL}")
    
try:
    if forms:
        scan_form_get(base_url, forms)
except:
    print(f"{Fore.RED}[error] Error occurred while scanning forms, finishing...{Style.RESET_ALL}")

# Print final results
def print_findings():
    if findings:
        print("\n\n==================Vulnerability Scan Results==================")
        for i, finding in enumerate(findings, 1):
            print(f"\n{Fore.GREEN}Finding #{i}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Type: {finding['type']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}URL: {finding['url']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Payload: {finding['payload']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Response Time: {finding['response_time']:.2f} seconds{Style.RESET_ALL}")
            if 'data' in finding:
                print(f"{Fore.GREEN}Data: {finding['data']}{Style.RESET_ALL}")
        print("===================================================")
        
        # save result file
        result_filename = f"{parsed_url.netloc}_result.txt"
        with open(result_filename, 'w') as f:
            json.dump(findings, f, indent=2)
        print(f"\nresult saved in {result_filename}")
    else:
        print("\nNo vulnerabilities found.")

# Print results after all scans complete
print_findings()
exit()

try:
    while True:
        pass
except KeyboardInterrupt:
    print_findings()
