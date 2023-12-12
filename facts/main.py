from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

text_splitter = CharacterTextSplitter(
    
)

loader = TextLoader("facts.txt")
docs = loader.load()

print(docs)