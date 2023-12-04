from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import argparse

load_dotenv()            # finds .env file in project & load it up, parse it

# 3. Parsing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--task", default="return a list of numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()


llm = OpenAI()

# 1. Create [prompt template]
code_prompt = PromptTemplate(
    template="Write a very short {language} function that will {task}",
    input_variables=["language", "task"]
)

# 2. Specify the [language model] to use 

code_chain = LLMChain(
    llm=llm, 
    prompt=code_prompt
)

# PromptTemplate requires a 'language' & a 'task'
result = code_chain({
    "language": args.language, 
    "task": args.task
})
print(result['text'])