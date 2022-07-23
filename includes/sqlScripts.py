##########################################################################################################################################################################
'''
                      This is scripts file which called from the server and worker side, where the queries are stored
'''
##########################################################################################################################################################################
class scripts:  
    # drop Events table
    drop_Events_table_if_exist = ''' DROP TABLE IF EXISTS Events;'''

   # create Events table
    create_Events_table_query = '''
                                CREATE TABLE IF NOT EXISTS Events (
                                    id INTEGER PRIMARY KEY,
                                    type TEXT NOT NULL,
                                    created_at datetime NOT NULL);
                                '''

   
    # drop Repos table
    drop_Repos_table_if_exist = ''' DROP TABLE IF EXISTS Repos;'''

    # create Repos table
    create_Repos_table_query = '''
                                CREATE TABLE IF NOT EXISTS Repos (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    url TEXT NOT NULL,
                                    event_id INTEGER NOT NULL);
                                '''
                            
   
    # drop PullRequests table   
    drop_PullRequests_table_if_exist = ''' DROP TABLE IF EXISTS PullRequests;'''

   # create PullRequests table
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

  
    # get the average time between a specific repo pr using id 
    get_avg_pr_time_using_repo_param = '''
                                        SELECT AVG(CAST ( (JulianDay(next_created_at) - JulianDay(created_at) ) * 24 * 60 AS INTEGER) ) 
                                        FROM (
                                                SELECT pr.created_at,
                                                        LEAD(pr.created_at, 1, pr.created_at) OVER (ORDER BY pr.created_at) AS next_created_at
                                                    FROM PullRequests pr
                                                    INNER JOIN Repos r 
                                                        ON r.event_id = pr.event_id
                                                    WHERE r.id = '@PARAM' OR 
                                                        INSTR(r.name, '@PARAM') > 0 OR 
                                                        INSTR(r.url, '@PARAM') > 0
                                            );                                
                                        '''                               

    # get max change time for specific repo or pr with a given param 
    get_max_pr_time_on_repo_using_pr_or_repo_param = '''
                                    SELECT max(pr.created_at) 
                                    FROM PullRequests pr
                                        INNER JOIN
                                        Repos r ON r.event_id = pr.event_id
                                    WHERE pr.id = '@VAR' OR 
                                        r.id = '@VAR' OR 
                                        INSTR(pr.url, '@VAR') > 0 OR 
                                        INSTR(node_id, '@VAR') > 0 OR 
                                        INSTR(html_url, '@VAR') > 0 OR 
                                        INSTR(diff_url, '@VAR') > 0 OR 
                                        INSTR(patch_url, '@VAR') > 0 OR 
                                        INSTR(issue_url, '@VAR') > 0 OR 
                                        INSTR(title, '@VAR') > 0 OR 
                                        INSTR(body, '@VAR') > 0 OR 
                                        INSTR(commits_url, '@VAR') > 0 OR 
                                        INSTR(r.name, '@VAR') > 0 OR 
                                        INSTR(r.url, '@VAR') > 0;
                                    '''                               


  # get all changes of prs happened on a speicic repo over time
    get_changes_over_time_for_specific_repo = '''
                                    SELECT e.created_at
                                    FROM Repos r
                                        INNER JOIN
                                        events e ON e.id = r.event_id
                                    WHERE r.id = '@VAR' OR 
                                        INSTR(r.name, '@VAR') > 0 OR 
                                        INSTR(r.url, '@VAR') > 0;
                                    '''


    # get count for each event tybe in db
    get_grouped_events = '''
                            SELECT type,
                                count(1) 
                            FROM events
                            WHERE created_at > DATETime('now', '-@OFFSET minutes') 
                            GROUP BY type;

                                '''                                                               