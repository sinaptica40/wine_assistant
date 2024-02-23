from flask import Blueprint, request
from src.SharedServices.MainService import MainService, StatusType
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)


import openai
import os

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

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

userApi = Blueprint('User view version 1', __name__)

@userApi.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        user_input = request.form['user_input']

        final_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="You are (Sergio) a Wine Expert. You having a conversation with a human. You have to answer only related to wine, if someone ask anything don't provide any information"
                ),  # The persistent system prompt
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # Where the memory will be stored.
                HumanMessagePromptTemplate.from_template(
                    "{description}"
                ),  # Where the human input will injected
            ]
        )

        chatOpenAI = ChatOpenAI(temperature=0.8, model_name="gpt-3.5-turbo",openai_api_key=os.getenv("OPENAI_KEY"))

        chain = LLMChain(
            llm=chatOpenAI,
            prompt=final_prompt,
            verbose=True,
            memory=memory
        )
        result = chain({"description": user_input})
        data = result.get('text', '')
        return data

    except openai.error.RateLimitError as e:
      return "Rate limit reached. Waiting for 20 seconds."
    except Exception as e:
      print(e)
      return "Something happened wrong. Please try again........."