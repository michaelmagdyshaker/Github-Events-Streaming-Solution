##########################################################################################################################################################################
'''
                      This is the core application backend side, where the scraping, db creation and filling the tables happen
'''
##########################################################################################################################################################################

from email import message
import requests
import os 
import sys
import sqlite3
from datetime import datetime
from time import sleep
from includes.sqlScripts import scripts

# set the database name in the current directory
db_name=os.getcwd() + '/github_events.db'
# set the interested events types
interested_types =['WatchEvent','PullRequestEvent','IssuesEvent']
# set the endpoint of public github events  
url = "https://api.github.com/events"
# declare the time period between each request in seconds
sleep_time =20


def scrape(url, interested_types):
    ''''
    input:
            - url: the endpoint of github events
            - interested_types: the list of event types to be filtered in the response before storing in the db
    behaviour: 
            - send request and get the response to github events endpoint
            - convert to the response into json
            - fiter for interested evenets  
    return: 
            - interested_events: the filtered response of the list of event types
    '''
    # get and clone the events from the github public endpoint    
    r = requests.get(url)
    # convert to json
    cont = r.json() 
    # the return list of filtered events
    interested_events=[]
    try:
        for t in range(len(cont)): 
            if cont[t]['type'] in (interested_types):
                interested_events.append(cont[t])
    
    # check id exceeded the requests rate
    except:
        if "API rate limit exceeded" in (r.json())['message']:
            sys.exit("you exceeded the requests rate!")
    
    # filter out the parsed cloned event types for each event
    return interested_events


def create_sql_db():
    ''''
    input: NONE
    behaviour: 
            - Establish a connection with SQLlight DB
            - Create Events, Repos and PullRequests tables
            - Close the connection
    return: None
    '''

    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        print("Database was created Successfully and Connected to SQLite")

       
        # cursor.execute(scripts.drop_Events_table_if_exist)
        cursor.execute(scripts.create_Events_table_query)
        # cursor.execute(scripts.drop_Repos_table_if_exist)
        cursor.execute(scripts.create_Repos_table_query)
        # cursor.execute(scripts.drop_PullRequests_table_if_exist)
        cursor.execute(scripts.create_PullRequests_table_query)
       
        # commit the changes in the db
        sqliteConnection.commit()

        print("Events, Repos and PullRequests tables are created successfully!")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            # Close the sql Connection
            sqliteConnection.close() 



def fill_db_tables(parsed_data,iteration):
    ''''
    input:
            - parsed_data: the filtered cloned events
            - iteration: the current request number
    behaviour: 
            - establish a connection with SQLlight DB
            - eterate over the events
            - parse the event into fields 
            - check if the type is PullRequestEvent to store the pr data of the event in PullRequests table
            - store the parsed fields into structured format in SQLlight DB
            - close the connection

    return: None
    '''
    try:
        # establish a sql connection 
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        # iterate over the parsed evnts
        for row in range(len(parsed_data)): 
            event_id = parsed_data[row]['id'] 
            type = parsed_data[row]['type']
            repo_id = parsed_data[row]['repo']['id']
            # cast to format of %Y-%m-%d %H:%M:%S
            created_at = (datetime.strptime((parsed_data[row]['created_at']), '%Y-%m-%dT%H:%M:%SZ')).strftime("%Y-%m-%d %H:%M:%S")
            repo_name =  parsed_data[row]['repo']['name']
            repo_url =  parsed_data[row]['repo']['url']
            # check if the event has type of PullRequestEvent to store its data
            if type =='PullRequestEvent':
                pr_id = parsed_data[row]['payload']['pull_request']['id']
                pr_url = parsed_data[row]['payload']['pull_request']['url']
                node_id = parsed_data[row]['payload']['pull_request']['node_id']
                html_url = parsed_data[row]['payload']['pull_request']['html_url']
                diff_url = parsed_data[row]['payload']['pull_request']['diff_url']
                patch_url = parsed_data[row]['payload']['pull_request']['patch_url']
                issue_url = parsed_data[row]['payload']['pull_request']['issue_url']
                number = parsed_data[row]['payload']['pull_request']['number']
                title = parsed_data[row]['payload']['pull_request']['title']
                # cast to format of %Y-%m-%d %H:%M:%S
                pr_created_at = (datetime.strptime((parsed_data[row]['payload']['pull_request']['created_at']), '%Y-%m-%dT%H:%M:%SZ')).strftime("%Y-%m-%d %H:%M:%S")
                pr_updated_at = (datetime.strptime((parsed_data[row]['payload']['pull_request']['updated_at']), '%Y-%m-%dT%H:%M:%SZ')).strftime("%Y-%m-%d %H:%M:%S")
                body = parsed_data[row]['payload']['pull_request']['body']
                commits_url = parsed_data[row]['payload']['pull_request']['commits_url']

                #insert PRs data
                cursor.execute('INSERT OR IGNORE INTO PullRequests values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [pr_id, pr_url, node_id, html_url, diff_url,patch_url,issue_url,number,title,pr_created_at,pr_updated_at,body,commits_url,event_id])
            #insert Events data
            cursor.execute('INSERT OR IGNORE INTO Events values(?,?,?)', [event_id, type, created_at]) 
            #insert Repos data
            cursor.execute('INSERT OR IGNORE INTO Repos values(?,?,?,?)', [repo_id, repo_name, repo_url, event_id]) 

        # commit the insertions operation
        sqliteConnection.commit()
        print( "data of batch {0} inserted Succefully".format(iteration))

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        # close the sql connection
        if sqliteConnection:
            sqliteConnection.close()



if __name__ == '__main__':
    
    print("Application and scrapping started successfully.. ")
    # create the db and construct the tables
    create_sql_db() 
    # initiate the iteration requests 
    iteration = 0
    # start the cloning and filling the db process
    while True:
        print('iteration: ',iteration)
        # send the requests and clone the events
        cont = scrape(url,interested_types)
        # fill the db 
        fill_db_tables(cont, iteration)
        # sleep after cloning for a period of time to pervent blockage
        sleep(sleep_time) 
        # increment the request iteration count
        iteration+=1


    