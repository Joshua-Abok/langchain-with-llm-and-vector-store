import sqlite3
from langchain.tools import Tool 

conn = sqlite3.connect("db.sqlite")


def run_sqlite_query(query):
    '''executed whenever chatGPT decides to execute a SQL query'''
    c = conn.cursor()    # similar to object allowing us access to the database
    try: 
        c.execute(query)
        return c.fetchall()  # collecting all the info the query returned
    except sqlite3.OperationalError as err: 
        return f"The following error occured: {str(err)}"

# set up the actual tool 
run_query_tool = Tool.from_function(
    name="run_sqlite_query",  # no spaces
    description="Run a sqlite query.",
        #  -> used by chatGPT to decide when to run the Tool
    func=run_sqlite_query
)

