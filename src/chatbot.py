import pinecone
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from langchain.agents import Tool
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
import password
from pinecone import Pinecone, ServerlessSpec
from langchain import hub
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage
from typing import AsyncIterator
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict
from langchain_core.runnables import RunnableBranch

os.environ['OPENAI_API_KEY'] = password.OPENAI_API_KEY
os.environ['PINECONE_API_KEY'] = password.PINECONE_API_KEY

store = {}

class Chatbot:
    def __init__(self,index_name):
        pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
        )   
        
        llm = ChatOpenAI(model='gpt-3.5-turbo')

        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

        vector_store = PineconeVectorStore(index_name=index_name,embedding=embeddings)

        retriever = vector_store.as_retriever(k=10)

        question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user's questions based on the below context:\n\n{context}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
        )

        query_transform_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            (
            "user",
            "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. Only respond with the query, nothing else.",
            ),
        ]
        )

        query_transforming_retriever_chain = RunnableBranch(
            (
                lambda x: len(x.get("messages", [])) == 1,
                # If only one message, then we just pass that message's content to retriever
                (lambda x: x["messages"][-1].content) | retriever,
            ),
            # If messages, then we pass inputs to LLM chain to transform the query, then pass to retriever
            query_transform_prompt | llm | StrOutputParser() | retriever,
        ).with_config(run_name="chat_retriever_chain")

        document_chain = create_stuff_documents_chain(llm, question_answering_prompt)

        conversational_retrieval_chain = RunnablePassthrough.assign(
            context=query_transforming_retriever_chain,
        ).assign(
            answer=document_chain,
        )

        self.agent = conversational_retrieval_chain

        self.history = ChatMessageHistory()


    async def query(self, query: str) -> AsyncIterator:
        self.history.add_user_message(query)
        response = await self.agent.ainvoke({"messages": self.history.messages})
        
        # Assuming response is already a stream, we'll just yield it directly
        yield response['answer']

        self.history.add_ai_message(response["answer"])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def parse_retriever_input(params: Dict):
    return params["messages"][-1].content