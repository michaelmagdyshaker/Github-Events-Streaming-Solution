##########################################################################################################################################################################
'''
                      This a e2e simulation file which call the restful apis based on the request parameter
                      Note: please MODIFY The repo_param or offset declared globally at first        
'''
##########################################################################################################################################################################import sqlite3

import requests

# set the local host 
Base = "http://127.0.0.1:5000/"
# set the restful api endpoint parameter for the first mertic (avg time between pr for a given parameter)
repo_param = 'repos'
# set the restful api endpoint parameter for the second and third mertics (total count for all grouped event types)
offset = 10000000

def send_request(req):
    ''''
    input:
            - req: the parameter indicate the metric number  
    behaviour: 
            - check the req number 
            - call api based on the req param 
                    Paramter to be sent to the server:
                    1 --> first metric : average time between pull requests for a given repository parameter
                    2 --> second metric : total number of events grouped by the event type for a given offset
                    3 --> bouns metric : Visualize for second metric
                    4 --> added metric : last pr for a given repository parameter
    return: - None
    '''

    if req == 1:
        response = requests.get(Base+"pr//" + repo_param.replace('/','__')) 
        print(response.json())
   
    elif req == 2: 
        response = requests.get(Base+"/events/" + str(offset)) 
        print(response.json())

    elif req == 3: 
        response = requests.get(Base+"/visualize/" + str(offset)) 
        print(response.json())

    elif req == 4: 
        response = requests.get(Base+"/lastchange/" + str(repo_param)) 
        print(response.json())
    else:
        print("sorry! invalid paramter, Please choose from 1 to 4")        


if __name__ == '__main__':
    # get the required metrics
    send_request(4)  

