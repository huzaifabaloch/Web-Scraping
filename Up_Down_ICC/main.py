from bs4 import BeautifulSoup 
from requests import get
import csv 

'''
* Scraping the cricinfo rankings page to retrieve icc t20 ranking of the teams.
* Storing the retrieved information in the csv file.
* Notify the user through emailing:
    * if a team has played a game.
    * if a team points increased or decreased.
    * if a team ranked up or down.
'''

def save_table_data(ranking):
    """
    # ? save the table t20 rankings in the csv file.
    """

    with open('rankings_t20.csv', 'w', newline='') as file_open:
        data_writer = csv.writer(file_open)
        data_writer.writerow(ranking.keys())
        for each_row in zip(*ranking.values()):
            data_writer.writerow(each_row)


def extract_keys(table_t20, rankings):
    """ 
    ? to extract headers from table and storing in a dictionary as keys.
    """

    for each_row in table_t20:
        #print(each_row.text)
        rankings.update({each_row.text:''})


def extract_t20_table_data(table_row, team, match, point, rating, ranking):
    """
    # ? to extract data from table like teams, points, ratings and stored them in a separate lists and then add as values 
    # ? to their specific header or key.
    """

    for key_row, row in enumerate(table_row):
        if key_row == 0:
            continue
    
        for k_data, data in enumerate(row.findAll('td')):
            if k_data == 0:
                team.append(data.text)
                ranking.update({'Team':team})
            elif k_data == 1:
                match.append(data.text)
                ranking.update({'Matches':match})
            elif k_data == 2:
                point.append(data.text)
                ranking.update({'Points':point})
            else:
                rating.append(data.text)
                ranking.update({'Rating':rating})

    return ranking

# * MAIN FUNCTION OF THIS SCRIPT
def start_scraping():
    
    rankings = {}           # * to store data of t20 table -> key as header and values as list of teams, matches, points, and ratings.
    teams = []              # * to store all teams names data.
    matches_played = []     # * to store match played data.
    ratings = []            # * to store ratings data.
    points = []             # * to store points data.

    # * the page that is going to be scraped.
    target_url = 'http://www.espncricinfo.com/rankings/content/page/211271.html'

    # ? user agent that acts on behalf of user, such as web browser that retieves interaction with the web.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    # * getting response and loading the webpage from server.
    response = get(target_url, headers = headers)

    # * created object to parse the html document.
    soup = BeautifulSoup(response.text, 'html.parser')

    # * find all the tables that contain object = StoryengineTable and stored in a list.
    # * every element in the list is a beautiful soup object, means we can retrive further tags, perfrom manipulation to it.
    icc_tables = soup.findAll('table', attrs={'class':'StoryengineTable'})

    # * stored third table i.e our target table (ICC T20 rankings) to a variable.
    icc_t20_table = icc_tables[2]

    extract_keys(icc_t20_table.findAll('hr'), rankings)
    table_rows = icc_t20_table.findAll('tr')
    rankings = extract_t20_table_data(table_rows, teams, matches_played, points, ratings, rankings)
    save_table_data(rankings)