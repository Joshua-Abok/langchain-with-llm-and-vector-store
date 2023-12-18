import sqlite3
from pydantic.v1 import BaseModel #pydantic lib - allows for annotation of different classes inside python class
                                            #   - clearly def what type of data we expect the class to receive as atts. 
from typing import List
from langchain.tools import Tool 

conn = sqlite3.connect("db.sqlite")


def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)


def run_sqlite_query(query):
    '''executed whenever chatGPT decides to execute a SQL query'''
    c = conn.cursor()    # similar to object allowing us access to the database

    # capture error of missing col 
    try: 
        c.execute(query)
        return c.fetchall()  # collecting all the info the query returned
    except sqlite3.OperationalError as err: 
        return f"The following error occured: {str(err)}"


# record says if you wanna get access to RunQueryArgsSchema u must provide a query attribute of string type
class RunQueryArgsSchema(BaseModel):
    query:str

# set up the actual tool 
run_query_tool = Tool.from_function(
    name="run_sqlite_query",  # no spaces
    description="Run a sqlite query.",
        #  -> used by chatGPT to decide when to run the Tool
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema  # provide the class to query tool
)


def describe_tables(table_names): 
    '''take list_tables and return info about the tables '''

    c = conn.cursor()
    tables = ', '.join("'" + table + "'" for table in table_names)
    # use tables inside our query to the db 
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)


# record says if you wanna get access to DescribeTablesArgsSchema u must provide a tables_names attribute of list of string values
class DescribeTablesArgsSchema(BaseModel):
    tables_names: List[str]

# wrap our describe_tables() inside a tool -> & then feed table to the agent :)
describe_tables_tool = Tool.from_function(
    name="describe_tables", 
    description="Given a list of table names, returns the schema of those tables", 
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema

)
