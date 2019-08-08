# this module allows to parse html.
from bs4 import BeautifulSoup as soup

# this module contains a function 'get' that will bring back the response from server to client for extracting data on that page.
# basically allow you to download the webpage.
from requests import get

# webpage to scrap.
url = 'http://www.espncricinfo.com/rankings/content/page/211271.html'

# to get the response from server for scraping. this will download the entire raw html page.
response = get(url)

''' 
created beautuful soup object to structure the code in html format.
the beautiful soup allows to parse html tags and retrieve useful information from it.
'''
b_soup = soup(response.text, 'html.parser')

# to find only one occurrence of table tag of oject/class (StoryengineTable).
rankings = b_soup.find('table', {'class':'StoryengineTable'})

# to find all the occurrence of tr tags and store in a list.
ranks = rankings.findAll('tr')

'''
looping through ranks that contain all the tr tags from first occurrence of table tag
with enumerate function that is used to loop through key and value pair.
we know that table contains table header and rows, in start k = 0 we will have header in our list
we find all occurrence of th - table head tag, then we loop through it to get the text out from each th tag and print them.
when k != 0, we know now we working with rows of data, so same way we find all occurrence of td -> table data tag and
and loop through and retrieve text out from them. formatting is used to show in tabular form.
'''
for k, r in enumerate(ranks):
    if k == 0:
        t_head = r.findAll('th')
        for h in t_head:
            print('{0:20}'.format(h.text), end='')
        print('\n')
    else:
        t_data = r.findAll('td')
        for d in t_data:
            print('{0:20}'.format(d.text), end='')
        print('\n')