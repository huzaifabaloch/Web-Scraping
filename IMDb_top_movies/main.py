from bs4 import BeautifulSoup
from requests import get
import csv
import json


class ImdbTopRatedMovies():
    """ To scrap top rated movies from IMDb """

    def __init__(self, url, header):
        """To initilize the scraping url and browser information(headers)."""

        self.url = url 
        self.header = header
        self.top_movies = {}

    def loading_content(self):
        """To download the content from target url to parse."""

        response = get(self.url, headers=header)
        if response.status_code != 200:
            return
        else:
            return response.text

    def parsing_fields(self):
        """To parse HTML to get mandatory fields."""

        # Fields
        ranks = []
        titles = []
        directors = []
        ratings = []
        total_user_ratings = []
        year_published = []
        image_links = []

        response_page = self.loading_content()
        if response_page == None:
            return
        
        # creating a soup object with passing page source code and displaying content using html parser.
        soup = BeautifulSoup(response_page, 'html.parser')

        # finding the table body where all top rated movies are present.
        table_body = soup.find('tbody', attrs={'class':'lister-list'})

        # iterating through each row in the table.
        for each_row in table_body.findAll('tr'):

            # getting all the image links.
            image_links.append(each_row.find('img')['src'])

            # finding all the anchor tags to extract the director name out of it.
            title_block = each_row.findAll('a')

            # extracting the director name from attribute title.
            directors.append(title_block[1]['title'])

            # finding and extracting text for the movie name, ranks, and year published and formatting.
            movie_details = each_row.find('td', {'class':'titleColumn'}).text.strip().split('\n')
            
            for key, each_detail in enumerate(movie_details):
                if key == 0:
                    ranks.append(int(each_detail.replace('.','')))
                elif key == 1:
                    titles.append(each_detail.strip())
                else:
                    year_published.append(int(each_detail.replace('(','').replace(')','')))

            # extracting the movie rating and total ratings that user rated.
            ratings.append(each_row.find('td', {'class':'ratingColumn imdbRating'}).text.strip())
            total_user_ratings.append(int(each_row.find('strong')['title'][13:-13].replace(',','').replace(',','')))

        return ranks, titles, directors, year_published, ratings, total_user_ratings, image_links

    def adding_to_dictionary(self):
        """Adding the data to the dictionary and saving as csv and json."""

        ranks, titles, directors, year_published, ratings, total_user_ratings, image_links = self.parsing_fields()

        self.top_movies.update({'Rank':ranks})
        self.top_movies.update({'Movie Name':titles})
        self.top_movies.update({'Director':directors})
        self.top_movies.update({'Year Published': year_published})
        self.top_movies.update({'Rating':ratings})
        self.top_movies.update({'Total Users Rated': total_user_ratings})
        self.top_movies.update({'Image links': image_links})

        with open('top_rated_movies.csv', 'w', newline='') as file_open:
            data_handler = csv.writer(file_open)
            data_handler.writerow(self.top_movies.keys())
            for each_row in zip(*self.top_movies.values()):
                data_handler.writerow(each_row)


target_url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

imdb = ImdbTopRatedMovies(target_url, header)
imdb.adding_to_dictionary()