import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time


queries = []
base_queries = []
forms = []

# url parse 
url = "http://127.0.0.1:5012/login"
# url = "https://redtiger.labs.overthewire.org/level1.php"

parsed_url = urlparse(url)
base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

print("url: ", url)
print("base_url: ", base_url)

def get_links_from_a_tag(url):
    # Get links from URL and check for endpoints
    re = requests.get(url, verify=False)  # Disable SSL certificate verification
    soup = BeautifulSoup(re.content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '?' in href:  
            if href.startswith('?'):  
                if href not in queries:  
                    queries.append(href)
            elif href.startswith('/'):  
                if href not in base_queries:  
                    base_queries.append(href)


def get_forms_from_form_tag(url):
    # Extract forms from URL
    re = requests.get(url, verify=False)
    soup = BeautifulSoup(re.content, 'html.parser')
    for form in soup.find_all('form'):
        action = form.get('action') if form.get('action') is not None else '/'
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

payloads = open("payloads.txt", "r").read().splitlines()

def scan_get(input_url, input_queries):
    for input_query in input_queries:
        # Measure base response time
        start_time = time.time()
        temp_response = requests.get(f"{input_url}{input_query}", verify=False)
        base_time = time.time() - start_time
        print(f"[info] Base response time for {input_url}{input_query}: {base_time:.2f} seconds")
        
        # Set threshold (2 times the base response time)
        threshold = max(2.0, base_time * 2)
        
        for payload in payloads:
            print("query: ", input_query)
            new_url = f"{input_url}{input_query} {payload}"
            print("new_url: ", new_url)
            
            # Measure payload execution time
            start_time = time.time()
            re = requests.get(new_url, verify=False)
            elapsed_time = time.time() - start_time
            
            # If response time exceeds threshold, potential vulnerability found
            if elapsed_time > threshold:
                print(f"[find]")
                print(f"URL: {new_url}")
                print(f"Payload: {payload}")
                print(f"Response time: {elapsed_time:.2f} seconds")
            else:
                print(f"[done] {new_url} - No issues found")

def scan_post(input_url, input_forms):
    pass

if queries:
    scan_get(url, queries)
if base_queries:
    scan_get(base_url, base_queries)
if forms:
    scan_post(base_url, forms)
