##########################################################################################################################################################################
'''
                      This is the routing file, where constructing the restful apis endpoint
'''
##########################################################################################################################################################################import sqlite3

from flask import Flask
from flask_restful import Api,Resource
import server 

app = Flask(__name__)
api =Api(app)


class Github_Events (Resource):
    # construct api endpoint for the first meteric (avg time between prs for a specific repo)
    @app.route("/pr/<string:repo>", methods=['GET', 'POST'])
    def get_avg_repo_time(repo):
        #call the get_avg_repo_time in the server side
        return(server.get_avg_repo_time(repo))
    
    # construct api endpoint for the second meteric (count of each event tybe)
    @app.route("/events/<int:offset>", methods=['GET', 'POST'])
    def get_total_number_of_events(offset):
        #call the get_total_number_of_events in the server side
        return(server.get_total_number_of_events(int(offset)))

    #construct api endpoint for the third meteric (covisualize a histogram for count of each event tybe)
    @app.route("/visualize/<int:offset>", methods=['GET', 'POST'])
    def visualize_total_number_of_events(offset):
        #call the visualize_total_number_of_events in the server side
        return(server.visualize_total_number_of_events(int(offset)))
        
    @app.route("/lastchange/<string:repo>", methods=['GET', 'POST'])
    def last_pr_on_repo(repo):
        #call the get_last_PR_on_repo in the server side
        return(server.get_last_PR_on_repo(repo))
    

if __name__ == '__main__':
    # start flask app service
    app.run(debug=True)


