from bs4 import BeautifulSoup
from requests import get
import csv
from itertools import zip_longest

url = 'https://www.alibaba.com/Products?spm=a2700.8293689.scGlobalHomeHeader.661.2ce265aaEkznXC'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

class Alibaba():
    """
    * To model a script that extracts all the links of the products by categories form alibaba.
    """

    def __init__(self, page_url, brower_information):
        """To initialize the url to be scraped and the client browser information."""

        self.page_url = page_url
        self.brower_information = brower_information
        self.links_by_category = {}

    def check_response_and_load_page(self):
        """To get the response of web from server and loading the page to an request object."""

        response = get(self.page_url, self.brower_information)
        if response.status_code == 200:
            return response.text
        else:
            return

    def parse_and_get_links(self):
        """To start parsing the page by creating beautiful soup object and extracting links."""

        category_headers = []
        product_list_by_category = {}
        products = []
        header_key = 0
        total_links = 0

        page = self.check_response_and_load_page()
        soup = BeautifulSoup(page, 'html.parser')

        # * main container that has all the producsts containers.
        main_container = soup.find('div', {'class':'cg-main'})

        # * storing product containers in a list.
        product_containers = main_container.findAll('div', {'class':'item util-clearfix'})

        # * grabbing all the headers from each category of links.
        for header in product_containers:
            category_headers.append(header.h3.text.strip())

        """
        ? first loop will iterate over each product container.
        ? in first product container, we find all the divs having css -> class:sub-item and we,
        ? iterate over each sub item.
        ? in first sub item, we find all the tags -> ul having class : sub-item-cout .... and,
        ? iterate over each of them.
        ? the final loop will select the first ul and find all the 'a' tags and from there,
        ? it find the href attribute and put that in a list and after add it to the dictionary,
        ? as key:value pair. 
        """
        for container in product_containers:
            for sub_item in container.findAll('div', {'class':'sub-item'}):
                for each_sub_item in sub_item.findAll('ul', {'class':'sub-item-cont util-clearfix'}):
                    for each_anchor_tag in each_sub_item.findAll('a'):
                        products.append(each_anchor_tag['href'])
                        product_list_by_category.update({category_headers[header_key]:products})
           
            header_key += 1
            products = []

            
        for product in product_list_by_category.values():
            total_links += len(product)
        print(total_links)

        with open('alibaba_product_links_by_category.csv', 'w', newline='') as file_open:
            data_writer = csv.writer(file_open)
            data_writer.writerow(product_list_by_category.keys())
            for each_row in zip_longest(*product_list_by_category.values()):
                data_writer.writerow(each_row)


alibaba_products_by_category = Alibaba(url, header)
alibaba_products_by_category.parse_and_get_links()
        



