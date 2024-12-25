from playwright.sync_api import sync_playwright
import time, requests

PROXY_USERNAME = "brd-customer-hl_5e532710-zone-residential"
PROXY_PASSWORD = "zh6ggn33j4mn"
PROXY_ADDRESS = "brd.superproxy.io:22225"  
 
def scrape_html_with_proxy(urls):
    html_content_dict = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(proxy={
            'server': f'http://{PROXY_ADDRESS}',
            'username': PROXY_USERNAME,
            'password': PROXY_PASSWORD
        }, headless=False) 
        

        for url in urls:
            try:

                response = requests.get(url, timeout=15)

                if response.status_code == 200:
                    html_content = response.text
                    print(f"Successfully retrieved content for {url} using requests.")


                    html_content_dict[url] = html_content
                else:
                    print(f"Requests failed with status {response.status_code}. ")


                

            except requests.RequestException as e:
                print(f"Requests error for {url}: {e}. Trying Playwright...")
    
        browser.close()
    

    return html_content_dict

# urls = ["https://berkeleyca.gov/", "https://en.wikipedia.org/wiki/Berkeley,_California"]

# scrape_html_with_proxy(urls)



























