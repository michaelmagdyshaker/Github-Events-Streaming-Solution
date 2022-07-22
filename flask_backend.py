from tokenize import String
from flask import Flask
from flask_restful import Api,Resource
import server 

app = Flask(__name__)
api =Api(app)


class Github_Events (Resource):
    @app.route("/pr/<string:repo>", methods=['GET', 'POST'])
    def get_avg_repo_time(repo):
        print(repo)
        return(server.get_avg_repo_time(repo))

    @app.route("/events/<int:offset>", methods=['GET', 'POST'])
    def get_total_number_of_events(offset):
        return(server.get_total_number_of_events(int(offset)))
    
    @app.route("/visualize/<int:offset>", methods=['GET', 'POST'])
    def visualize_total_number_of_events(offset):
        return(server.visualize_total_number_of_events(int(offset)))

if __name__ == '__main__':
    app.run(debug=True)


