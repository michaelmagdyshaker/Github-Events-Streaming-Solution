import requests
import json
import os 
import sys
import sqlite3
from datetime import datetime
from time import sleep
from includes.sqlScripts import scripts

db_name=os.getcwd() + '/github_events.db'

interested_types =['WatchEvent','PullRequestEvent','IssuesEvent']
url = "https://api.github.com/events"


def scrape(url, interested_types):
    print (db_name)
    r = requests.get(url)
    if "https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting" in r: # exceeded the limit
        print("you exceeded the requests limit!")
        sys.exit() 
  
    cont = r.json()
    interested_events=[]
    for t in range(len(cont)):
        if cont[t]['type'] in (interested_types):
            interested_events.append(cont[t])
    return interested_events


def create_sql_db():

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

        sqliteConnection.commit()

        print("Events, Repos and PullRequests tables are created successfully!")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



def fill_db_tables(parsed_data,iteration):
    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        
        for row in range(len(parsed_data)):
            event_id = parsed_data[row]['id'] 
            type = parsed_data[row]['type']
            repo_id = parsed_data[row]['repo']['id']
            created_at = (datetime.strptime((parsed_data[row]['created_at']), '%Y-%m-%dT%H:%M:%SZ')).strftime("%Y-%m-%d %H:%M:%S")
            repo_name =  parsed_data[row]['repo']['name']
            repo_url =  parsed_data[row]['repo']['url']
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
                pr_created_at = parsed_data[row]['payload']['pull_request']['created_at']
                pr_updated_at = parsed_data[row]['payload']['pull_request']['updated_at']
                body = parsed_data[row]['payload']['pull_request']['body']
                commits_url = parsed_data[row]['payload']['pull_request']['commits_url']

                cursor.execute('INSERT OR IGNORE INTO PullRequests values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [pr_id, pr_url, node_id, html_url, diff_url,patch_url,issue_url,number,title,pr_created_at,pr_updated_at,body,commits_url,event_id])

            cursor.execute('INSERT OR IGNORE INTO Events values(?,?,?)', [event_id, type, created_at])
            cursor.execute('INSERT OR IGNORE INTO Repos values(?,?,?,?)', [repo_id, repo_name, repo_url, event_id])


        sqliteConnection.commit()
        print( "data of batch {0} inserted Succefully".format(iteration))

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



if __name__ == '__main__':
    
    print("Application and scrapping started successfully.. ")

    create_sql_db()

    iteration = 0
    while True:
        print('iteration: ',iteration)
        cont = scrape(url,interested_types)
        fill_db_tables(cont, iteration)
        sleep(30) #to pervent github blockage
        iteration+=1


    