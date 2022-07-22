import requests
Base = "http://127.0.0.1:5000/"
repo_param = 'repos'
offset = 10000000



def send_request(req):
    if req == 1:
        response = requests.get(Base+"pr//" + repo_param.replace('/','__')) 
        print(response.json())
   
    elif req == 2: 
        response = requests.get(Base+"/events/" + str(offset)) 
        print(response.json())

    elif req == 3: 
        response = requests.get(Base+"/visualize/" + str(offset)) 
        print(response.json())

    else:
        print("sorry! invalid paramter, Please put from 1, 2 or 3")        


if __name__ == '__main__':
    
    '''
        Paramter to be sent to the server:
                1 --> first metric : average time between pull requests for a given repository parameter
                2 --> second metric : total number of events grouped by the event type for a given offset
                3 --> bouns metric : Visualize for second metric
        
        please, MODIFY The repo_param or offset declared globally at first        
    '''
    send_request(3) # to get the required metrics 

