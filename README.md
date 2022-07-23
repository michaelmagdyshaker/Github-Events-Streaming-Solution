# Github Events Streaming Solution 

Streaming and filter out three types of events from Github API and calculate metrics over the data then constuct restful APIs


![image](https://user-images.githubusercontent.com/24366936/180618355-61defdc9-a5f8-4a6c-8f02-605445b5ce82.png)

## Description
*here is the steps of the application
- Scraping the row events from pupblic Github API
- Fitle for a specifc types (WatchEvent, PullRequestEvent and IssuesEvent)
- Create a sql light DB and use data modeling concepts to create an data model and pipeline
- Parse the data into structre format
- Save it into sql light db
- Calculates metrics and quering on them 
- Get some ueful insights and visualizations and answer qustions.
- Consrruct an enpoints for restful APIs using Flask
    - (host+"/pr/<string:repo>")
    - (host+"/"/events/<int:offset>")
    - (host+"/visualize/<int:offset>")
    - (host+"/lastchange/<string:repo>")
    
    ![c4_d](https://user-images.githubusercontent.com/24366936/180619132-52813eb8-9958-460d-8c19-b1f96546d41c.png)

### Getting Started
* just clone the repo locally from https://github.com/michaelmagdyshaker/lely_assignment
* download SQLlight studio to interface with the database from https://sqlitestudio.pl/ then import github_events.db file
* works on any os
* ensure of localhost in main_test.py if you want to test the app locally  

## Prerequisites & Installing
* requests
  ```sh
  pip install requests
  ```
* sqlite3
  ```sh
  pip install sqlite3
  ```
* flask
  ```sh
  pip install flask
  ```
* matplotlib
  ```sh
  pip install matplotlib
  ```

### Executing program

* clone and setup the dependices
* run worker.py file sepreately before start the flask application (give it minutes to fill the db )
    note: close it after finishing (like the fridge door) cause your ip will be blocked from the github events api 
  ```
     python worker.py
  ```

* run flask_backend.py to start the services (using termenal)
  ```
     python main_test.py
  ```
* to test the apis manually, execute main_test.py after setting the desired api request param(1,2,3,4) and setting the repo or offset parameter globally.  
  ```
     python main_test.py
  ```
* send requests to the provided endpoints above using postman or any testing tool
* in the front-end, the param after the routing endpoint will be replace with a special character "__" to handle the forward slashes
* enjoy the results and visuals :) 

![image](https://user-images.githubusercontent.com/24366936/180618113-dfb596fa-0603-4e85-b703-4888b95b948a.png)
![image](https://user-images.githubusercontent.com/24366936/180619287-efc1d8ee-3d32-475a-a837-03f4cac3b3a8.png)
![image](https://user-images.githubusercontent.com/24366936/180619313-76d8f2c8-4590-4196-b46d-1b9e332c6313.png)
![image](https://user-images.githubusercontent.com/24366936/180619509-1f536e74-ebec-4bb7-a724-195fac8fe671.png)


## Help
contct michael.magdyy96@gmail.com

## Authors

michael magdy 

## Version History

* 0.1
    * Initial Release 2022-07

