from langchain.vectorstores import Chroma 
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()


# create our chat model 
chat = ChatOpenAI()
embeddings = OpenAIEmbeddings()

# instance of chroma for similarity_search but not add contents to db
db = Chroma(
    persist_directory="emb", 
    embedding_function=embeddings
)

# set RetrievalQA construct in langchain
# retriever -> object that take in string & return relevant docs 
retriever = db.as_retriever()

chain = RetrievalQA.from_chain_type(
    llm=chat, 
    retriever=retriever, 
    chain_type="stuff" #take some context from the vector store & "stuff" it into the prompt
)

result = chain.run("What is an interesting fact about the English language")

print(result)
