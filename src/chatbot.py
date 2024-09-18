import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain import OpenAI
from langchain.agents import Tool
import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

class Chatbot:
    def __init__(self,index_name):
        index = Pinecone.from_existing_index(index_name,OpenAIEmbeddings(model="text-embedding-ada-002"))

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), index.as_retriever(), memory=self.memory)

        tools = [
        Tool(
            name='Knowledge Base',
            func=qa.run,
            description=(
                'use this tool when answering climate legislation queries'
            )
        )
        ]

        llm = ChatOpenAI(
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model_name='gpt-3.5-turbo',
        temperature=0.0
        )

        self.agent =  initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        early_stopping_method='generate',
        memory=self.memory 
        )

    def query(self, query):
        return self.agent(query)['output']