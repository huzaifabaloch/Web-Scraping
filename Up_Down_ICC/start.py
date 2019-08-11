import os
import csv
import smtplib

import main as m

teams_updated = {}

def second_file_exists():
    """
    * this will check if older csv file for icc_rankings exists.
    * if not creates second csv file and copy the data to it from,
    * current extracted data from main.py.

    * if file already exists (old icc t20 rankings file), then it means
    * maybe the current csv file is updated from main.py and new rankings 
    * are updated and rankings are listed in current file.
    * we grab both current and old csv files data into two separate lists
    * for manipulation.
    """

    old_rankings = []
    current_rankings = []

    if not os.path.isfile('rankings_t20_old.csv'):
        with open('rankings_t20.csv', 'r') as file_open:
            reader = csv.reader(file_open)
            for each_row in reader:
                old_rankings.append(each_row)

        with open('rankings_t20_old.csv', 'w', newline='') as file_open:
            writer = csv.writer(file_open)
            for each_row in old_rankings:
                writer.writerow(each_row)
    else:
        with open('rankings_t20_old.csv', 'r') as file_open:
            reader = csv.reader(file_open)
            for each_row in reader:
                old_rankings.append(each_row)  
                
        with open('rankings_t20.csv', 'r') as file_open:
            reader = csv.reader(file_open)
            for each_row in reader:
                current_rankings.append(each_row)    
    
    return current_rankings, old_rankings


def get_updated_teams():
    """
    * the main purpose to get updated teams and their data.
    * zipped the new and old list of data that will pair first element
    * of list 1 with first element of list 2 and so on.

    * the inner loop is used if icc t20 data are updated from web and teams
    * positions are changed. it will handle that.
    * select the first item from new list and check its existance from old list
    * until it is retrieved then simply checking the values for
        * match played
        * points
        * ratings
    * store them in a separate dictionary with teams name that are updated. NOT FOR ALL.
    """

    m.start_scraping()
    
    current_rankings, old_rankings = second_file_exists()
    key = 0

    for current, old in zip(current_rankings, old_rankings):
        if key == 0:
            key += 1
            continue

        for item in range(len(old)):

            if current[0] == old[item]:
                match = point = rating = ''
            
                if int(current[1]) > int(old[1]):
                    match = current[1]
            
                if int(current[2]) > int(old[2]):
                    point = current[2]
            
                if int(current[3]) > int(old[3]):
                    rating = current[3]

                if match != '' or point != '' or rating != '':
                    teams_updated.update({current[0]:[match, point, rating]})
            
                break
            break

    if teams_updated:
       send_mail() 


def send_mail():
    """
    * sending email about updated data.
    """

    k = 0

    try:
        # ? establishing a connection between gmail and our connection.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('huzbaudi3@gmail.com', 'qvqpnmzvxcwpkmqq')

        subject = 'ICC T20 rankings updated.'

        body = 'The following data has been updated.\n'

        
        for key, values in teams_updated.items():
            body += key
            k = 0
            for each_val in values:

                if k == 0 and each_val != '':
                    message = f' has played total of {each_val} games.'
                    body += message 
                elif k == 1 and each_val != '':
                    message = f' Ratings are {each_val}.'
                    body += message
                elif k == 2 and each_val != '':
                    message = f' Points are {each_val}. '
                    body += message
                
                k += 1
        
        body += '\n\nCheck out more..\n' + 'http://www.espncricinfo.com/rankings/content/page/211271.html'

        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            'huzbaudi3@gmail.com',
            'huzbaudi3@gmail.com',
            message,
        )
        print('Email has been sent!')
        server.quit()
    except:
        print('Some problem while sending email!')


# * RUN SCRIPT
get_updated_teams()