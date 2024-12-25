import os
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_main_domain(url):
    try:
        netloc = urlparse(url).netloc
        # Split by '.' and get the second-to-last part, which is usually the main domain
        parts = netloc.split('.')
        if len(parts) >= 2:
            return parts[-2]  # e.g., 'wikipedia' in 'en.wikipedia.org'
    except Exception as e:
        print(f"Error parsing URL {url}: {e}")
    return None

def format_date(date_str):
    # date string in 'YYYY-MM-DD' format
    return date_str[5:] + date_str[4] + date_str[0:4]

def is_url_allowed(url, include_filters, exclude_filters):
    # check for inclusion filters
    if include_filters:
        allowed = any(inc_filter in url for inc_filter in include_filters)
        if not allowed:
            return False

    # check for exclusion filters
    if exclude_filters:
        excluded = any(excl_filter in url for excl_filter in exclude_filters)
        if excluded:
            return False

    return True

def perform_search(query, start_date, end_date, include_websites, exclude_websites, num_pages=10):
    search_results = [] #url's

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # need run in headless because the server can't have browsers opening 
        page = browser.new_page()

        for page_number in range(num_pages):
            #10 pages for 100 links
            start_index = page_number * 10

            #google url based on page #
            url = f"https://www.google.com/search?q={query}&tbs=cdr:1,cd_min:{format_date(start_date)},cd_max:{format_date(end_date)}&start={start_index}"

            print(f"Scraping page {page_number + 1}: {url}")

            page.goto(url)
            page.wait_for_load_state('networkidle')

    
            html = page.content()

            #parse page content
            soup = BeautifulSoup(html, 'html.parser')

            #link extraction
            for result in soup.select('h3'):
                parent_link = result.find_parent('a')
                link = parent_link['href']
                if is_url_allowed(link, include_websites, exclude_websites):
                    search_results.append(link)
    
                # 100 links for testing purposes
                if len(search_results) >= 100:
                    break
        browser.close()
    
    return search_results



























def scrape_urls(urls):
    scraped_date = {}

    for url in urls:
        def scrape_multiple_urls(urls):
            scraped_data = {}
            for url in urls:
                print(f"Scraping URL: {url}")
                html_content = get_html_content(url)
                if html_content:
                    scraped_data[url] = html_content
                else:
                    print(f"Failed to retrieve content from {url}")
    
    return scraped_data


