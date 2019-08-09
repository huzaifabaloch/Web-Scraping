from bs4 import BeautifulSoup as soup
from requests import get
import csv
from itertools import zip_longest


courses = {}

url = 'https://www.w3schools.com/'

response = get(url)

b_soup = soup(response.text, 'html.parser')

# - main block - from where we need to extract the data.
block = b_soup.find('div', {'class':'w3-bar-block'})

# finding all the tags inside the - main block - and storing it.
children = block.findChildren()

# finding all the heading tags.
headings = block.findAll('h4', {'class':'w3-margin-top'})

# iterating through each tag/child and extacting the text out of it and printing.
for child in children:

        # heading is coming two times. for avoiding that we use this condition.
        if child.h4:
                sub_head = []
                continue

        # heading part -> this is done for newline, if one section finishes, we add newline then move to next section.
        elif child in headings:
                head = child.text

        # subheadings.
        else:
                sub_head.append(child.text)
                courses.update({head:sub_head})


with open('w3schools_courses.csv', 'w', newline='') as fp:
        wr = csv.writer(fp)
        wr.writerow(courses.keys())#writes title row'
        # iteratable function that unzip first element of list 1 with other lists first elements and stores as a tuple/list and increments
        # to second item and repeat.
        wr.writerows(zip_longest(*courses.values()))