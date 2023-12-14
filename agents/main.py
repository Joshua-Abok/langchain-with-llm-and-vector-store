from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate, 
    HumanMessagePromptTemplate, 
    MessagesPlaceholder
)

from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool


load_dotenv()

chat = ChatOpenAI()
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template("{input}"), 
        MessagesPlaceholder(variable_name="agent_scratchpad")
            #   -> looks for input variable with "agent_scratchpad" name & then find some data assigned to the 
            #      variable_name & then explode to some greater no. of messages 
            #      agent_scratchpad -> simplified form of memory (keeps track with convo with chatGPT)
    ]
)


# refactor -> variable for tools 
tools = [run_query_tool]

agent = OpenAIFunctionsAgent(
    llm=chat, 
    prompt=prompt, 
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent, 
    verbose=True, 
    tools=tools
)

agent_executor("How many users are in the database?")
