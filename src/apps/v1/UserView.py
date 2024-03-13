from flask import Blueprint, request
from src.SharedServices.MainService import MainService, StatusType
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)
from langchain.chains import RetrievalQA

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

import openai
import os
import time
import re

# Chat prompt template
from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate
)

# Langchain classes
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

import json
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    MessagesPlaceholder

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

userApi = Blueprint('User view version 1', __name__)

def parse_output(description):
    #description        =   description.replace("I am Assistant, a large language model trained by OpenAI.","I am Meera, a Trained Assistant by Owebest.")

    # Replace links with <a> tags
    description = re.sub(r'(https?://\S+)', r'<a target="_blank" href="\1">\1</a>', description)
    # Replace email addresses with mailto links
    #description = re.sub(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'<a href="mailto:\1">\1</a>', description)
    # Replace phone numbers with tel links
    #description = re.sub(r'(\+?[0-9]+[-\s]?)+', r'<a href="tel:\1">\1</a>', description)

    return description

print(os.getenv('OPENAI_KEY'))
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_KEY')

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

app = Flask(__name__)
static_dir_path = os.path.join(app.root_path, 'static')

if PERSIST and os.path.exists("wine_db"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="wine_db", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  loader = DirectoryLoader(static_dir_path+"/data")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"wine_db"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

# Build prompt
from langchain.prompts import PromptTemplate
template = """You are (Lorenzo) a Wine Expert. stop providing information outside of retriever. Please limit of the answer maximum 130 token.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)


turbo_llm = ChatOpenAI(temperature=0.8, model_name="gpt-3.5-turbo",openai_api_key=os.getenv("OPENAI_KEY"))

chain = RetrievalQA.from_chain_type(turbo_llm,
                                retriever=index.vectorstore.as_retriever(),
                                return_source_documents=True,
                                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
                                
@userApi.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        user_input = request.form['user_input']

        
        """ chain = LLMChain(
            llm=chatOpenAI,
            prompt=final_prompt,
            verbose=True,
            memory=memory
        ) """
        """ result = chain({"description": user_input})
        data = result.get('text', '')
        return data """

        result = chain({"query": user_input})
        response        =   parse_output(result["result"])
        html_text = '<html>\n<body>\n'

        for line in response.split('\n'):
            html_text += f'<p>{line}</p>\n'

        html_text += '</body>\n</html>'
        return {"voice_text":result["result"],"html_text":html_text}

    except openai.error.RateLimitError as e:
      return {"voice_text":"Rate limit reached. Waiting for 20 seconds","html_text":"Rate limit reached. Waiting for 20 seconds"}
    except Exception as e:
      print(e)
      return {"voice_text":"Something happened wrong. Please try again.........","html_text":"Something happened wrong. Please try again........."}