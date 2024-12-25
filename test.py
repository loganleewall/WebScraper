import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def format_date(date_str):
    return date_str[5:] + date_str[4] + date_str[0:4]

def perform_search(query, start_date, end_date, include_websites, exclude_websites, num_pages=10):
    search_results = []
    html_content = []  # To store HTML content from each page

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=False for debugging
        page = browser.new_page()

        for page_number in range(num_pages):
            # Calculate the start index for pagination (10 results per page)
            start_index = page_number * 10

            # Formulate the Google search URL with pagination
            url = f"https://www.google.com/search?q={query}&tbs=cdr:1,cd_min:{format_date(start_date)},cd_max:{format_date(end_date)}&start={start_index}"

            print(f"Scraping page {page_number + 1}: {url}")

            # Visit the Google search URL
            page.goto(url)

            # Wait for the search results to load
            page.wait_for_selector('h3', timeout=60000)

            # Get the page content (HTML) and store it
            html = page.content()
            html_content.append(html)  # Store HTML for each page

            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Extract links from search results
            for result in soup.select('h3'):
                link = result.find_parent('a')['href']
                
                # Apply inclusion/exclusion filters if necessary
                if (not include_websites or any(site in link for site in include_websites)) and not any(site in link for site in exclude_websites):
                    search_results.append(link)

                # Stop when we have 100 links
                if len(search_results) >= 100:
                    break

            if len(search_results) >= 100:
                break  # Stop pagination when we have 100 links

            # Optional: Add a delay between requests to avoid triggering Google's anti-scraping mechanisms
            page.wait_for_timeout(2000)  # 2 second delay

        # Close the browser after scraping
        browser.close()

    return search_results, html_content

# Example usage:
query = "AI tools"
start_date = "01-01-2023"
end_date = "12-31-2023"
include_websites = []  # Specify websites to include (optional)
exclude_websites = []  # Specify websites to exclude (optional)

# Scrape the first 10 pages to get 100 links and the HTML content of each page
links, html_pages = perform_search(query, start_date, end_date, include_websites, exclude_websites, num_pages=10)

# Prepare the data to be saved as JSON
data = {
    "query": query,
    "start_date": start_date,
    "end_date": end_date,
    "total_links": len(links),
    "links": links
}

# Save the results as a JSON file
with open("search_results.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(links)} links, saved as 'search_results.json'.")
