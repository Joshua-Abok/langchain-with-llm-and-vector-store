from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

    # memory set up
memory = ConversationBufferMemory(memory_key="messages", return_messages=True)  

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"], 
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(
    llm=chat, 
    prompt=prompt,
    memory=memory      #wire up memory with the chat
)
while True: 
    content = input(">> ")

    result = chain({"content": content})
    print(result["text"])