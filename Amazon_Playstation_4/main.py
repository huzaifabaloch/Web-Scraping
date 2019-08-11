from bs4 import BeautifulSoup
from requests import get
import csv


class Playstation4():
    """To scrap the first page of amazon playstation 4 games and store in a csv file."""

    def __init__(self, url, header):
        """To initialize the url and the browser information."""

        self.url = url
        self.header = header


    def get_page(self):
        """To get response from server and load the webpage."""

        response = get(self.url, headers=self.header)
        if not response.status_code == 200:
            return
        else:
            return response


    def extract_document(self):
        """To extract PS4 data from amazon and collect useful information from it."""
        """
        * JUST A REMAINDER TO MYSELF WHEN WORKING WITH WEBSITES LIKE AMAZON.
        ? For everyone who has problems using amazon.com: .com makes the html code with javascript. 
        ? You can trick them with using 2 soups. Load soup1 like in this video. 
        ? Then load soup2 with soup1.prettify(). 
        ? Then you got soup2 loaded correctly and you can do all the fun stuff.
        """
        amazon_ps4_games = []  # * To store each list of game that contains game description, price and producer.
        response = self.get_page()
        soup = BeautifulSoup(response.text, 'html.parser')
        soup2 = BeautifulSoup(soup.prettify(), 'html.parser')

        # * To find the section of page where all the games data present.
        page_block = soup2.find('div', {'class':'s-result-list s-search-results sg-row'})  

        # * To find all the game blocks. Each block will contain name, price, shipping, producer and others. 
        game_block = page_block.findAll('div', {'class':'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28'})

        
        for each_game in game_block:
            game = []
            description = each_game.h2.text.strip()
            game.append(description)
            print(description)

            if not each_game.find('span', {'class':'a-offscreen'}):
                price = ''
            else:
                price = each_game.find('span', {'class':'a-offscreen'}).text[1:] # cutoff the $ symbol.

            game.append(price)
            print(price)
            
            if not each_game.find('div', {'class':'a-row a-size-base a-color-secondary'}):
                # * if there is no such tag in that block, just assign empty string to producer.
                producer = ''
                game.append(producer)
                print(producer)

            elif each_game.find('div', {'class':'a-row a-size-base a-color-secondary'}).text.strip()[0:4] == 'Only':
                # * Some tags contain information other than producer, like Only 2 left, to avoid this we find the,
                # * that string and match it with ours and assign producer an empty string.
                producer = ''
                game.append(producer)
                print(producer)

            else:
                producer = each_game.find('div', {'class':'a-row a-size-base a-color-secondary'}).text
                game.append(producer)
                print(producer)
            
            # * Add each game data into this list.
            amazon_ps4_games.append(game)
        
        return amazon_ps4_games


    def save_data(self, amazon_ps4_data):

        with open('ps4_games.csv', 'w', newline='') as file_open:
            headers = ['Game Description', 'Price($)', 'Producer']
            data_writer = csv.writer(file_open)
            data_writer.writerow(headers)
            data_writer.writerows(amazon_ps4_data)


header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
url = 'https://www.amazon.com/s?i=videogames-intl-ship&bbn=16225016011&rh=n%3A%2116225016011%2Cn%3A6427814011&dc&fst=as%3Aoff&qid=1565518577&rnid=16225016011&ref=lp_16225016011_nr_n_0'

ps4_games = Playstation4(url,header)
amazon_ps4_data = ps4_games.extract_document()
ps4_games.save_data(amazon_ps4_data)