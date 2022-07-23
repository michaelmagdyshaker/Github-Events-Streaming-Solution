##########################################################################################################################################################################
'''
                      This is the application server side, where quering on the database and the getting the metrics happen
'''
##########################################################################################################################################################################import sqlite3
from datetime import datetime,timedelta
import time
from numpy import rec
import pandas as pd
import matplotlib.pyplot as plt
import os
from time import sleep
from includes.sqlScripts import scripts
from flask import Flask
from flask_restful import Api,Resource
from matplotlib import dates as mdates
import sqlite3

# set the database name in the current directory
db_name=os.getcwd() + '/github_events.db'

def get_avg_repo_time(repo):
    ''''
    input:
            - repo: the parameter sent from the user to search in the repos fields 
    behaviour: 
            - Establish a connection with SQLlight DB
            - check over all fields (id,name,URL) over all repos to get the created_at of it's prs
            - get the avg time between al prs
            - close the connection 
    return: 
            - return_string: a json/dic string which contains the average time between pull requests for a specific repo with a given param
    '''
    repo = repo.replace('__','/')
    sqliteConnection = sqlite3.connect(db_name)
    cursor = sqliteConnection.cursor()
    return_string = ""
    try:
        cursor.execute(((scripts.get_avg_pr_time_using_repo_param).replace('@PARAM',str(repo))))
        record = cursor.fetchall()

        if record[0][0] is None :
            print("No Repo found with parameter contains '{0}'".format(repo))
            return_string = ("No Repo found with parameter contains {0}".format(repo))

        else:
            print("average time between pull requests for repo contains: '{0}' = {1} minutes".format(repo, record[0][0]))
            return_string = ("average time between pull requests repo contains: '{0}' = {1} minutes".format(repo, record[0][0]))

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return_string = ("Error while connecting to sqlite", error)
  
    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()

    return {"return":return_string}




def get_last_PR_on_repo(repo):
    ''''
    input:
            - repo: the parameter sent from the user to search in the repos and prs fields 
    behaviour: 
            - Establish a connection with SQLlight DB
            - check over all fields of Repos (id,name,URL) and Most of PR fileds  to get the maximum created_at/ change of the prs
            - close the connection 
    return: 
            - return_string: a json/dic string which contains the average time between pull requests for a specific repo with a given param
    '''
    repo = repo.replace('__','/')
    sqliteConnection = sqlite3.connect(db_name)
    cursor = sqliteConnection.cursor()
    return_string = ""
    try:
        cursor.execute(((scripts.get_max_pr_time_on_repo_using_pr_or_repo_param).replace('@VAR',str(repo))))
        record = cursor.fetchall()

        if record[0][0] is None :
            print("No Repo or PR found with parameter contains '{0}'".format(repo))
            return_string = ("No Repo or PR found with parameter contains {0}".format(repo))

        else:
            print("last Pullrequest happened on repo or pr contains: '{0}' was on {1}".format(repo, record[0][0]))
            return_string = ("last Pullrequest happened on repo or pr contains: '{0}' was on {1}".format(repo, record[0][0]))

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return_string = ("Error while connecting to sqlite", error)

    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()

    return {"return":return_string}



def get_changes_over_time_for_repo(repo):
    ''''
    input:
            - repo: the parameter sent from the user to search in the repos and prs fields 
    behaviour: 
            - Establish a connection with SQLlight DB
            - get all changes/pr happened on a specifc repo
            - close the connection 
    return: 
            - return_string: a json/dic string which contains the average time between pull requests for a specific repo with a given param
    '''
    repo = repo.replace('__','/')
    sqliteConnection = sqlite3.connect(db_name)
    cursor = sqliteConnection.cursor()
    dates=[]
    try:
        cursor.execute(((scripts.get_changes_over_time_for_specific_repo).replace('@VAR',str(repo))))
        record = cursor.fetchall()

        if record == []:
            print("No Repo found with parameter contains '{0}'".format(repo))

        else:
            # print("changes over time for repo parameter contains: '{0}' = {1}".format(repo, record))
            # return_string = ("changes over time for repo parameter contains: '{0}' = {1}".format(repo, record))
            dates=[]
            for i in range(len(record)):
                dates.append(record[i][0])
            print("changes over time for repo parameter contains '{0}' = {1}".format(repo, dates))
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return_string = ("Error while connecting to sqlite", error)
  
    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()

    return {repo:dates}



def get_total_number_of_events(offset):

    ''''
    input:
            - offset: the parameter sent from the user to look back for a period of time in minutes
    behaviour: 
            - establish a connection with SQLlight DB
            - query over the db to get the total count of each event type for a period of time
            - close the connection
    return: 
            - dic: a dictionary of a string contains the total count of each event type in the db
    '''
    # establish a connection with sqllight
    sqliteConnection = sqlite3.connect(db_name)
    cursor = sqliteConnection.cursor()
    # declare the return of of the sql query
    record = []
    # the return of the function
    return_string = ""

    try:
        # execute the query to get the total count of each event type for a period of time
        cursor.execute(((scripts.get_grouped_events).replace('@OFFSET',str(offset))))
        # get the result of the query 
        record = cursor.fetchall()
        # handle if no events in the db
        if record == []:
            print("No event found for the past {0} minutes!".format(offset))
            return_string = ("No event found for the past {0} minutes!".format(offset))
        else:
            # iterate over types in the db and get each type's count
            for i in range(len(record)):
                print("count of {0} events = {1} for the past {2} minutes".format(record[i][0], record[i][1], offset))
                return_string = return_string + ("count of {0} events = {1} for the past {2} minutes".format(record[i][0], record[i][1], offset)) +"\n"

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return_string = ("Error while connecting to sqlite", error)
    # close the connection
    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()
    # convert the result into dictionary to be serialized in json response         
    dic={}
    if not record ==[]:
        for i in range(len(record)):
            dic[record[i][0]] =record[i][1]

    return dic



def visualize_total_number_of_events(offset):
    ''''
    input:
            - offset: the parameter sent from the user to look back for a period of time in minutes to be sent to @get_total_number_of_events function
    behaviour: 
            - call get_total_number_of_events and get each type count
            - plot the data in a visualized figure
    return: 
            - dic: the result in dictionary format just for logging 
    '''
    # call to get each type count for the past offset minutes
    dic = get_total_number_of_events(offset)
    # handle if there are no events in the db
    if dic =={}:
        print("No event found for the past {0} minutes!".format(offset))
        return ("No event found for the past {0} minutes!".format(offset))
    else: 
        # split the result into two lists ti be figured
        names = list(dic.keys())
        values = list(dic.values())
        # plot the data in a histogram
        plt.bar(range(len(dic)), values, tick_label=names)
        plt.xlabel('Type')
        plt.ylabel('Count')
        plt.suptitle("count for each type for the past {0} minutes".format(offset))
        plt.show()
    return dic

