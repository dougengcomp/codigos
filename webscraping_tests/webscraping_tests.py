import requests
import bs4
import pdb

def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

#function for checking when there are no quotes left:
def end_of_site(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,"lxml")
    no_quotes = soup.select("div")
    text=str (no_quotes[5])
    if text.find("No quotes found!")>-1:
        print ("end of site detected")
        return True
    return False

#TASK: Get the names of all the authors on the first page.
def get_authors_names_for_a_page(url):
    list_of_authors=[]
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,"lxml")
    quotes_with_authors = soup.select('div.quote small.author')
    for item in quotes_with_authors:
        authors_name= item.get_text()
        list_of_authors.append(authors_name)
    list_of_authors=sorted(set(list_of_authors))
    return list_of_authors

#task get names of all authors in all pages:
def get_authors_names_for_all_pages (url):
    all_authors_available=[]
    i=1
    while not (end_of_site(url.format(i))):
        print (f"entrando na {i}a iteracao")
        all_authors_available.append (get_authors_names_for_a_page (url.format(i)))
        all_authors_available=sorted(set((flatten_list (all_authors_available))))
        print (f"round {i} after set: {all_authors_available} ")
        print (f"amount of unique authors is: {len(all_authors_available)}")
        i+=1
        continue
    return all_authors_available

#TASK: Create a list of all the quotes on the first page.
def get_all_quotes_1st_page(url):
    list_of_quotes=[]
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,"lxml")
    quotes = soup.select('div.quote span.text')
    for item in quotes:
        quotes_text= item.get_text()
        list_of_quotes.append(quotes_text)
    return list_of_quotes

#TASK: retrieve the "top ten" tags
def get_top_ten_tags(url):
    list_of_tags=[]
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,"lxml")
    tags = soup.select('span.tag-item a.tag')
    for item in tags:
        tag_text= item.get_text()
        list_of_tags.append(tag_text)
    return list_of_tags



base_url = 'https://quotes.toscrape.com/page/{}/'

print (get_top_ten_tags(base_url.format(1)))
#print (get_all_quotes_1st_page(base_url.format(1)))
#get_authors_names_for_all_pages (base_url)



""""    
for book in books:
if len(book.select('.star-rating.Two')) != 0:
two_star_titles.append(book.select('a')[1]['title'])
print (two_star_titles) 
"""