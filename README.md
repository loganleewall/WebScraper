# WebScraper
Evabot News Web Scraper
This is a contract project I completed for a sales AI startup, Evabot. 

The project is a Flask-based application to automate the retrieval, extraction, and parsing of articles from
Google search results using custom queries and date filters

I leveraged Playwright and Beautiful Soup libraries to achieve a processing rate of ~100 links per minute

To bypass firewalls and CAPTCHAs, I utilized BrightData’s residential proxy infrastructure to achieve 87.4% access success rate for target sites.

To run the script, run the app.py file. This file calls on functions within search.py to aggregate a list of 100 URLs that are subject to the user search and filteres. 
Then, contentScrape.py goes through the proxy to scrape the HTML content from each link.
Finally, contentParse.py parses the HTML to extract the date, title, and a description. The results are outputted in a dictionary within a JSON file. 
