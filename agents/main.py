from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate, 
    HumanMessagePromptTemplate, 
    MessagesPlaceholder
)
from langchain.schema import SystemMessage    # helps make plain, simple system mess without any templating
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool # importing the list_tables function
from tools.report import write_report_tool


load_dotenv()

chat = ChatOpenAI()

tables = list_tables()
# print(tables)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to a SQLite database. \n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
            
            )),
        HumanMessagePromptTemplate.from_template("{input}"), 
        MessagesPlaceholder(variable_name="agent_scratchpad")
            #   -> looks for input variable with "agent_scratchpad" name & then find some data assigned to the 
            #      variable_name & then explode to some greater no. of messages 
            #      agent_scratchpad -> simplified form of memory (keeps track with convo with chatGPT)
    ]
)


# refactor -> variable for tools 
tools = [
         run_query_tool, 
         describe_tables_tool, 
         write_report_tool
         ]

# chain that knows how to use tools 
# -> take list of tools & convert 'em into JSON function descr. 
# -> has input var, memory, prompts, etc - all stuff that a CHAIN has. 
agent = OpenAIFunctionsAgent(
    llm=chat, 
    prompt=prompt, 
    tools=tools
)

# takes an agent and runs it until the response is not a function call -> while loop
agent_executor = AgentExecutor(
    agent=agent, 
    verbose=True, 
    tools=tools
)

# agent_executor("How many shipping addresses are in the database?")
agent_executor("Summarize the top 5 most popular products. Write the results to a report file.")

