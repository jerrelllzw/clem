import json

# Define json fields
FIELD_PAPER_ID = 'paper_id'
FIELD_AUTHORS = 'authors'
SUBFIELD_AUTHORS_FNAME = 'fname'
SUBFIELD_AUTHORS_LNAME = 'lname'
SUBFIELD_AUTHORS_CAUTHOR = 'cauthor'
SUBFIELD_AUTHORS_EMAIL = 'email'
FIELD_YEAR = 'year'
FIELD_PAPER = 'paper'
SUBFIELD_PAPER_TITLE = 'title'
SUBFIELD_PAPER_KEYWORDS = 'keywords'
FIELD_SOURCE = 'source'
SUBFIELD_SOURCE_JOURNAL = 'journal'
SUBFIELD_SOURCE_VOLUME = 'volume'
SUBFIELD_SOURCE_NUMBER = 'number'
SUBFIELD_SOURCE_PAGES = 'pages'
SUBFIELD_SOURCE_PAGES_START = 's_page'
SUBFIELD_SOURCE_PAGES_END = 'e_page'

# Load the data
def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("File not found")
        return None
    except json.decoder.JSONDecodeError:
        print("Invalid JSON")
        return None
    except Exception as e:
        print("Unknown error:", str(e))
        return None


def search_by_year(data, year):
    return [publication for publication in data if publication[FIELD_YEAR] == int(year)]

def search_by_name(data, partial_names):
    partial_names = set(partial_names.lower().split())
    return [publication for publication in data for author in publication[FIELD_AUTHORS] 
            if partial_names.intersection(author[SUBFIELD_AUTHORS_FNAME].lower().split() + author[SUBFIELD_AUTHORS_LNAME].lower().split())]

def search_by_author_lastname(data, lastNames):
    lastNames = set(lastNames.lower().split())
    return [publication for publication in data for author in publication[FIELD_AUTHORS] 
            if lastNames.intersection(author[SUBFIELD_AUTHORS_LNAME].lower().split())]

def search_by_author_firstname(data, firstNames):
    firstNames = set(firstNames.lower().split())
    return [publication for publication in data for author in publication[FIELD_AUTHORS] 
            if firstNames.intersection(author[SUBFIELD_AUTHORS_FNAME].lower().split())]

def search_by_journal(data, journal_words):
    return [publication for publication in data if journal_words.lower() in publication[FIELD_SOURCE][SUBFIELD_SOURCE_JOURNAL].lower()]

def search_by_title(data, title_words):
    return [publication for publication in data if title_words.lower() in publication[FIELD_PAPER][SUBFIELD_PAPER_TITLE].lower()]

def search_by_keyword(data, keyword_words):
    keyword_words = keyword_words.lower().split()
    matching_publications = []

    for publication in data:
        keyword_list = [k.lower() for k in publication[FIELD_PAPER][SUBFIELD_PAPER_KEYWORDS]]
        for word in keyword_words:
            if any(word in k for k in keyword_list):
                matching_publications.append(publication)
                break  

    return matching_publications

def search_by_paper_id(data, paper_id):
    results = []
    for publication in data:
        if str(publication.get('paper_id', '')) == str(paper_id):
            results.append(publication)
    return results

def search_by_pages(data, pages):
    publications = [publication for publication in data if (FIELD_SOURCE in publication and SUBFIELD_SOURCE_PAGES in publication[FIELD_SOURCE])]
    results = []
    for publication in publications:
        if SUBFIELD_SOURCE_PAGES_END in publication[FIELD_SOURCE][SUBFIELD_SOURCE_PAGES] and SUBFIELD_SOURCE_PAGES_START in publication[FIELD_SOURCE][SUBFIELD_SOURCE_PAGES]:
            e_page = publication[FIELD_SOURCE][SUBFIELD_SOURCE_PAGES][SUBFIELD_SOURCE_PAGES_END]
            s_page = publication[FIELD_SOURCE][SUBFIELD_SOURCE_PAGES][SUBFIELD_SOURCE_PAGES_START]
            if isinstance(e_page, int) and isinstance(s_page, int):
                if e_page - s_page == pages:
                    results.append(publication)
    return results

'''
#def search_by_keyword(data, keyword_words):
    keyword_words = keyword_words.lower().split()
    matching_publications = []

    for publication in data:
        keyword_list = [k.lower() for k in publication[FIELD_PAPER][SUBFIELD_PAPER_KEYWORDS]]
        for word in keyword_words:
            if any(word in k for k in keyword_list):
                matching_publications.append(publication)
                break  

    return matching_publications

#import json

author_search1 = input("Please key in a first author last name to search for:")
author_search2 = input("Please key in a second author last name to search for:")

print ()

f = open("master.json", encoding="utf8")

publications = json.loads(f.read())

i = 0

for publication in publications:
    author_list = []
    for author in publication["authors"]:
        author_list.append(author["lname"])
    if author_search1 in author_list and author_search2 in author_list:                         # Boolean "AND"
        print ("Paper ID:", publication ["paper_id"])
        print (publication["paper"]["title"])
        print ("\n")
        i = i + 1

print (f"\nAuthors with last name {author_search1} and {author_search2}, published {i} article(s) together.")
            
f.close()


#Search by keywords
#Search by number of pages
#Search by two authors names'''
