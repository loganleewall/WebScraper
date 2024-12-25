import json
from flask import Flask, render_template, request, jsonify
from search import perform_search
from contentScrape import scrape_html_with_proxy
from contentParse import parse_article_info


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        start_date = request.form['start_date']  # 'YYYY-MM-DD' format
        end_date = request.form['end_date']      # 'YYYY-MM-DD' format
        include_websites = request.form.getlist('include_websites')
        exclude_websites = request.form.getlist('exclude_websites')

        ## string processing the inclusion/exclusion inputs
        if include_websites != [""]:
            include_websites = [website.strip().lower().strip() for website in include_websites[0].split(",")]
        else:
            include_websites = []
        if exclude_websites != [""]:
            exclude_websites = [website.strip().lower().strip() for website in exclude_websites[0].split(",")]
        else:
            exclude_websites = []
        print(include_websites, exclude_websites)

        links = perform_search(query, start_date, end_date, include_websites, exclude_websites)


        searchdataFormat = {
        "query": query,
        "start_date": start_date,
        "end_date": end_date,
        "total_links": len(links),
        "links": links
        }


        ## dumping structured search url data into json file
        with open("search_results.json", "w", encoding="utf-8") as searchFile:
            json.dump(searchdataFormat, searchFile, ensure_ascii=False, indent=4)


        ## scraping the html content from  urls 
        rawHTML = scrape_html_with_proxy(links)

        ## parsing html for relevant info 
        parsedarticles = parse_article_info(rawHTML)

        ## dumping relevant html content into json
        with open("parsed_html.json", "w", encoding="utf-8") as parsedHTMLFile:
            json.dump(parsedarticles, parsedHTMLFile, ensure_ascii=False, indent=4)


        
        ## TO-DO

        ## 1 - Lower the date fail rate (use Evabot's current function)

        ## 2 - Dump code to BitBucket
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
