class scripts:  
    
    drop_Events_table_if_exist = ''' DROP TABLE IF EXISTS Events;'''

   
    create_Events_table_query = '''
                                CREATE TABLE IF NOT EXISTS Events (
                                    id INTEGER PRIMARY KEY,
                                    type TEXT NOT NULL,
                                    created_at datetime NOT NULL);
                                '''

   
   
    drop_Repos_table_if_exist = ''' DROP TABLE IF EXISTS Repos;'''

  
    create_Repos_table_query = '''
                                CREATE TABLE IF NOT EXISTS Repos (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    url TEXT NOT NULL,
                                    event_id INTEGER NOT NULL);
                                '''
                            
   
   
    drop_PullRequests_table_if_exist = ''' DROP TABLE IF EXISTS PullRequests;'''

   
    create_PullRequests_table_query = '''
                                CREATE TABLE IF NOT EXISTS PullRequests (
                                    id INTEGER PRIMARY KEY,
                                    url TEXT NOT NULL,
                                    node_id TEXT ,
                                    html_url TEXT,
                                    diff_url TEXT,
                                    patch_url TEXT,
                                    issue_url TEXT,
                                    number INTEGER,
                                    title TEXT,
                                    created_at datetime NOT NULL,
                                    updated_at datetime NOT NULL,
                                    body TEXT,
                                    commits_url TEXT,
                                    event_id INTEGER NOT NULL
                                    );
                                '''

  
  
    get_avg_pr_time_using_id = '''
                                SELECT AVG(CAST ( (JulianDay(next_created_at) - JulianDay(created_at) ) * 24 * 60 * 60 AS INTEGER) ) 
                                FROM (
                                        SELECT created_at,
                                               LEAD(created_at, 1, created_at) OVER (ORDER BY created_at) AS next_created_at
                                            FROM PullRequests
                                            WHERE id = @ID
                                    );
                                '''                               

     
    get_avg_repo_time_using_freetxt = '''
                                SELECT AVG(CAST ( (JulianDay(next_created_at) - JulianDay(created_at) ) * 24 * 60 * 60 AS INTEGER) ) 
                                FROM (
                                        SELECT created_at,
                                                LEAD(created_at, 1, created_at) OVER (ORDER BY created_at) AS next_created_at
                                            FROM PullRequests
                                            WHERE INSTR(url, '@VAR') > 0 OR 
                                                INSTR(node_id, '@VAR') > 0 OR 
                                                INSTR(html_url, '@VAR') > 0 OR 
                                                INSTR(diff_url, '@VAR') > 0 OR 
                                                INSTR(patch_url, '@VAR') > 0 OR 
                                                INSTR(issue_url, '@VAR') > 0 OR 
                                                INSTR(title, '@VAR') > 0 OR 
                                                INSTR(body, '@VAR') > 0 OR 
                                                INSTR(commits_url, '@VAR') > 0
                                    );

                                '''                               
  
    get_avg_repo_time_using_number = '''
                                SELECT AVG(CAST ( (JulianDay(next_created_at) - JulianDay(created_at) ) * 24 * 60 * 60 AS INTEGER) ) 
                                FROM (
                                        SELECT created_at,
                                               LEAD(created_at, 1, created_at) OVER (ORDER BY created_at) AS next_created_at
                                            FROM PullRequests
                                            WHERE number = @NUM
                                    );
                                '''



    get_grouped_events = '''
                            SELECT type,
                                count(1) 
                            FROM events
                            WHERE created_at > DATETime('now', '-@OFFSET minutes') 
                            GROUP BY type;

                                '''                                                               
