from flask import Flask, render_template, request, jsonify,redirect, url_for
from searchEngine import (
    load_data,
    search_by_authors,
    search_by_pages, 
    search_by_year, 
    search_by_name, 
    search_by_author_lastname, 
    search_by_author_firstname, 
    search_by_journal, 
    search_by_title, 
    search_by_keyword,
    search_by_paper_id
)
import json

HTML_FILE = 'index.html'
DATABASE_NAME = './master.json'
KEY_FULLNAME = 'fullname'
KEY_FIRSTNAME = 'firstname'
KEY_LASTNAME = 'lastname'
KEY_YEAR = 'year'
KEY_JOURNAL = 'journal'
KEY_JOURNAL_ARTICLE_TITLE = 'journalarticletitle'
KEY_KEYWORD = 'keyword'
KEY_PAPER_ID = 'paper_id'
KEY_S_PAGE = 's_page'
KEY_E_PAGE = 'e_page'


# To start webapp
app = Flask(__name__)

# web_app_url/<route>

@app.route('/')
def index():
    return render_template(HTML_FILE)

# submit button sends a http post request to web_app_url/search. This function the handles the request
@app.route('/search', methods=['POST'])
def search():
    search_data = request.json
    dataBase = load_data(DATABASE_NAME)
    matching_publications = []
    #matching_publications = dataBase  # Start with all publications
    print(search_data)
    
    isAndSearch = True if search_data.get('searchType') == 'and' else False
    
    if isAndSearch:
        matching_publications = dataBase  # Start with all publications
        for key, value in search_data.items():
            if value == '':
                continue
            elif key == KEY_FULLNAME:
                matching_publications = [pub for pub in matching_publications if pub in search_by_name(dataBase, value)]
            elif key == KEY_FIRSTNAME:
                matching_publications = [pub for pub in matching_publications if pub in search_by_author_firstname(dataBase, value)]
            elif key == KEY_LASTNAME:
                matching_publications = [pub for pub in matching_publications if pub in search_by_author_lastname(dataBase, value)]
            elif key == KEY_YEAR:
                matching_publications = [pub for pub in matching_publications if pub in search_by_year(dataBase, value)]
            elif key == KEY_JOURNAL:
                matching_publications = [pub for pub in matching_publications if pub in search_by_journal(dataBase, value)]
            elif key == KEY_JOURNAL_ARTICLE_TITLE:
                matching_publications = [pub for pub in matching_publications if pub in search_by_title(dataBase, value)]
            elif key == KEY_KEYWORD:
                matching_publications = [pub for pub in matching_publications if pub in search_by_keyword(dataBase, value)]
            elif key == KEY_PAPER_ID:  
                matching_publications = [pub for pub in matching_publications if pub in search_by_paper_id(dataBase, value)]
    else:
        for key in search_data.keys():
            if search_data[key] == '':
                continue
            elif key == KEY_FULLNAME:
                matching_publications += search_by_name(dataBase, search_data[key])
            elif key == KEY_FIRSTNAME:
                matching_publications += search_by_author_firstname(dataBase, search_data[key])
            elif key == KEY_LASTNAME:
                matching_publications += search_by_author_lastname(dataBase, search_data[key])
            elif key == KEY_YEAR:
                matching_publications += search_by_year(dataBase, search_data[key])
            elif key == KEY_JOURNAL:
                matching_publications += search_by_journal(dataBase, search_data[key])
            elif key == KEY_JOURNAL_ARTICLE_TITLE:
                matching_publications += search_by_title(dataBase, search_data[key])
            elif key == KEY_KEYWORD:
                matching_publications += search_by_keyword(dataBase, search_data[key])
            elif key == KEY_PAPER_ID:  
                matching_publications += search_by_paper_id(dataBase, search_data[key])
        matching_publications = removeDuplicates(matching_publications)
    
    return jsonify(matching_publications)

def removeDuplicates(publications):
    seen = set()
    unique_publications = []
    for publication in publications:
        pub_id = publication.get('paper_id', '')
        if pub_id not in seen:
            unique_publications.append(publication)
            seen.add(pub_id)
    return unique_publications

@app.route('/advanced_search')
def advanced_search():
    return render_template('advanced_search.html')

@app.route('/advanced_search/results', methods=['POST'])
def advanced_search_results():
    search_data = request.json
    dataBase = load_data(DATABASE_NAME)
    year = search_data.get('year')
    condition = search_data.get('condition')
    authors = search_data.get('authors')
    pages = search_data.get('pages')
    if year != '':
        year = int(year)
        if condition == "before":
            matching_publications = [pub for pub in dataBase if int(pub[KEY_YEAR]) < year]
        elif condition == "after":
            matching_publications = [pub for pub in dataBase if int(pub[KEY_YEAR]) > year]
        elif condition == "equals":
            matching_publications = [pub for pub in dataBase if int(pub[KEY_YEAR]) == year]
        elif condition == "before_or_equals":
            matching_publications = [pub for pub in dataBase if int(pub[KEY_YEAR]) <= year]
        elif condition == "after_or_equals":
            matching_publications = [pub for pub in dataBase if int(pub[KEY_YEAR]) >= year]
        else:
            print(matching_publications)
            return jsonify({"error": "Invalid search condition"})
    elif authors != '':
        matching_publications = search_by_authors(dataBase, authors)
    elif pages != '':
        pages = int(pages)
        matching_publications = search_by_pages(dataBase, pages)
    #print(matching_publications)
    return jsonify(matching_publications)

if __name__ == '__main__':
    app.run(debug=True, port=3000)

