from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()

# emb = embeddings.embed_query("hi there")

# print(len(emb))  -> outputs the embeds. 

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=0
)

loader = TextLoader("facts.txt")
docs = loader.load_and_split(
    text_splitter=text_splitter
)

    # create a new chroma db & store all the embeddings for our docs inside it 
db = Chroma.from_documents(
    docs,      # creating an instance for chroma to create embed for the "docs"
    embedding=embeddings, 
    persist_directory="emb"  # embeds stored in sqlite db inside the emb dir
)
            
            # similarity_search_with_score
results = db.similarity_search(
    "What is an interesting fact about the english language?"
    # k=1   # most relevant for four results
                                           )

for result in results: 
    print("\n")
    # print(result[1])
    # print(result[0].page_content)
    print(result.page_content) 