import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv


load_dotenv()

## Langsmith Tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OPENAI"


#Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant please response to the user queries"),
        ("user","Question:{question}")

    ]
)


def generate_response(question,api_key,model,temperature,max_tokens):

    


    try: 

        openai.api_key = api_key
        llm = ChatOpenAI(model=model,temperature=temperature,max_tokens=max_tokens)

        outputParser = StrOutputParser()

        chain = prompt|llm|outputParser

        return chain.invoke({'question':question})
    except Exception as e:

        print(e)

        return "Error in API keys"


st.title("Langchain Demo with OPENAI API")

input_text = st.text_input("Search the topic you want")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter API Key",type='password')

model = st.sidebar.selectbox('Select an Open AI model',['gpt-4o','gpt-4-turbo','gpt-3.5-turbo'])

temp = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Token Size",min_value=20,max_value=1000,value=400)




if input_text:
    st.write(generate_response(input_text,api_key,model,temp,max_tokens))

    

