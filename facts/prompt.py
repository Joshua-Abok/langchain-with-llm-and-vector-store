from langchain.vectorstores import Chroma 
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
# invoking custom retriever
from redundant_filter_retriever import RedundantFilterRetriever
from dotenv import load_dotenv
import langchain

langchain.debug = True

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
# call our custom retriever ->  RedundantFilterRetriever instead of db.as_retriever()
retriever = RedundantFilterRetriever(
    # pass in customized attributes -> embeddings & chroma
    embeddings=embeddings,
    chroma=db
)

# retriever = db.as_retriever()

chain = RetrievalQA.from_chain_type(
    llm=chat, 
    retriever=retriever, 
    chain_type="stuff" #   refine -> build an initial response, then give the LLM an opport. to update it with further context 
            #   "map_reduce" -> build a summary of each doc, then feed each summary to final qn
            #   "stuff"      -> take some context from the vector store & "stuff" it into the prompt
            #   "map_rerank" -> find relevant part of each doc & give it a score of how relevant it is  
)

result = chain.run("What is an interesting fact about the English language")

print(result)
