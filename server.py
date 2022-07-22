import sqlite3
from numpy import rec
import pandas as pd
import matplotlib.pyplot as plt
import os
from time import sleep
from includes.sqlScripts import scripts
from flask import Flask
from flask_restful import Api,Resource

db_name=os.getcwd() + '/github_events.db'

def get_avg_repo_time(repo):
    repo = repo.replace('__','/')
    sqliteConnection = sqlite3.connect(db_name)
    cursor = sqliteConnection.cursor()
    return_string = ""
    if str(repo).isdigit() and len(str(repo)) > 4: #check if it's for PR id, usually constructed of 10 digits
        try:
            cursor.execute(((scripts.get_avg_pr_time_using_id).replace('@ID',str(repo))))
            record = cursor.fetchall()

            if record[0][0] is None:
                print("No PR found with id = {0}".format(repo))
                return_string = ("No PR found with id = {0}".format(repo))

            else:
                print("average time between pull requests for repo with id: {0} = {1}".format(repo, record[0][0]))
                return_string = ("average time between pull requests for repo with id: {0} = {1}".format(repo, record[0][0]))

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return_string = ("Error while connecting to sqlite", error)
  
    elif str(repo).isdigit() and len(str(repo)) <= 4: #chck if it's for number parameter
        try:
            cursor.execute(((scripts.get_avg_repo_time_using_number).replace('@NUM',str(repo))))
            record = cursor.fetchall()

            if record[0][0] is None:
                print("No PR found with number = {0}".format(repo))
                return_string = ("Error while connecting to sqlite", error)
            else:
                for i in range(len(record)):
                    print("average time between pull requests for repo with number: {0} = {1}".format(repo, record[0][0]))
                    return_string = return_string + ("average time between pull requests for repo with number: {0} = {1}".format(repo, record[0][0])) 
        
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return_string = ("Error while connecting to sqlite", error)
 
    else:
        try:
            cursor.execute(((scripts.get_avg_repo_time_using_freetxt).replace('@VAR',str(repo))))
            record = cursor.fetchall()

            if record[0][0] is None:
                print("No PR found with parameter = {0}".format(repo))
                return_string = ("No PR found with id = {0}".format(repo))
            
            else:
                for i in range(len(record)):
                    print("average time between pull requests for repo with param: {0} = {1}".format(repo, record[i][0]))
                    return_string = return_string + ("average time between pull requests for repo with number: {0} = {1}".format(repo, record[0][0])) 

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return_string = ("Error while connecting to sqlite", error)
 
    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()

    return {"return":return_string}


def get_total_number_of_events(offset):
   
    sqliteConnection = sqlite3.connect(db_name)
    cursor = sqliteConnection.cursor()
    record = []
    return_string =""

    try:
        cursor.execute(((scripts.get_grouped_events).replace('@OFFSET',str(offset))))
        record = cursor.fetchall()
        if record == []:
            print("No event found for the past {0} minutes!".format(offset))
            return_string = ("No event found for the past {0} minutes!".format(offset))
        else:
            for i in range(len(record)):
                print("count of {0} events = {1} for the past {2} minutes".format(record[i][0], record[i][1], offset))
                return_string = return_string + ("count of {0} events = {1} for the past {2} minutes".format(record[i][0], record[i][1], offset)) +"\n"

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return_string = ("Error while connecting to sqlite", error)

    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()
    dic={}
    if not record ==[]:
        for i in range(len(record)):
            dic[record[i][0]] =record[i][1]

    return dic


def visualize_total_number_of_events(offset):
    dic = get_total_number_of_events(offset)
    if dic =={}:
        print("No event found for the past {0} minutes!".format(offset))
        return ("No event found for the past {0} minutes!".format(offset))
    else: 
        names = list(dic.keys())
        values = list(dic.values())

        plt.bar(range(len(dic)), values, tick_label=names)
        plt.xlabel('Type')
        plt.ylabel('Count')
        plt.suptitle("count for each type for the past {0} minutes".format(offset))
        plt.show()
    return dic


