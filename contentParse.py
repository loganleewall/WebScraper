from bs4 import BeautifulSoup
import re
from dateutil import parser

def find_dates(text):
    """
    Extract and parse the first valid date from the input text based on multiple patterns.
    """
    date_patterns = [
        # Various date formats
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b',
        r'\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b',
        r'\b\d{4}-\d{2}-\d{2}\b',
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b\d{1,2}\.\d{1,2}\.\d{4}\b',
        r'\b\d{1,2}-\d{1,2}-\d{4}\b',
        r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec), \d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec) \d{1,2}, \d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec) \d{4}\b',
        r'\b\d{1,2}-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)-\d{4}\b',
        r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December), \d{1,2}, \d{4}\b'
    ]

    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        if matches:
            try:
                # Parse and standardize the first matched date
                parsed_date = parser.parse(matches[0], fuzzy=True)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                print(f"Error parsing date: {matches[0]}")

    return None

def parse_article_info(html_content_dict):
    extracted_data = {"output":[]}

    for url, html in html_content_dict.items():
        if not html:
            print(f"No content for URL: {url}")
            continue

        soup = BeautifulSoup(html, 'html.parser')

        # extract title, description, date

        title = soup.find('title').get_text() if soup.find('title') else None
        if not title:
            title = soup.find('h1').get_text() if soup.find('h1') else None

        description_tag = soup.find('meta', attrs={"name": "description"})
        description = description_tag['content'] if description_tag else None

        date = None
        date_tag = soup.find('meta', attrs={"property": "article:published_time"})
        if date_tag:
            date = date_tag['content']
        else:
            time_tag = soup.find('time')
            if time_tag:
                date = time_tag.get('datetime') or time_tag.get_text()

        if not date:
            text_content = soup.get_text(separator=" ", strip=True)
            date = find_dates(text_content)
        
        curDict = { "url": url,
                    "title": title, 
                    "description": description,
                    "published_date": date
                    }
        extracted_data["output"].append(curDict)

    return extracted_data
