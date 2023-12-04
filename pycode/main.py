from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain # help series chain together
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

                #  chain in series with SequentialChain - 1. [prompt template]
test_prompt = PromptTemplate(
    input_variables=['language', 'code'],
    template='Write a test for the following {language} code: \n {code}'
)


# 2. Specify the [language model] to use 

code_chain = LLMChain(
    llm=llm, 
    prompt=code_prompt,
    output_key="code"    # instead of default "text"
)

                #  chain in series with SequentialChain - 2. [language model]
test_chain = LLMChain(
    llm=llm, 
    prompt=test_prompt, 
    output_key="test"
)

                #  chain in series with SequentialChain - 3. wire the chains together - code_chain & test_chain
chain = SequentialChain(
    chains=[code_chain, test_chain], 
    input_variables=["task", "language"], 
    output_variables=["test", "code"]
)                

# PromptTemplate requires a 'language' & a 'task'
result = chain({
    "language": args.language, 
    "task": args.task
})

print(">>>>>> GENERATED CODE:")
print(result["code"])

print(">>>>>> GENERATED TEST:")
print(result["test"])