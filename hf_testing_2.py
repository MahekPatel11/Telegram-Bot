from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

os.environ["HF_TOKEN"] =  os.getenv("HF_TOKEN")
os.environ["LANGCHAIN_API_KEY"] =  os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] =  os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

HF_TOKEN = os.getenv("HF_TOKEN")

st.title("Langchain joke generator")
st.markdown("Powered by huggingface")

topic = st.text_input("enter topic for joke!")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "you are a joke genearting assisatant . Generate only one joke on the given topic and donot continue the conversation "),
        ("user" , "{topic}")
    ]
)

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=HF_TOKEN
)

output_parser = StrOutputParser()

chain = prompt|llm|output_parser

if topic:
    with st.spinner("genearting your joke ...."):
        response = chain.invoke({"topic":topic})
        st.success("here is your genearted joke")
        st.write(response.strip())