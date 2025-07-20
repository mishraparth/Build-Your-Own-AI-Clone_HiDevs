# app.py

import streamlit as st
import os
from dotenv import load_dotenv

# --- Langchain Core Components ---
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# --- Load Environment Variables ---
# This line loads the API key from the .env file
load_dotenv()

# --- App Title and Configuration ---
st.set_page_config(page_title="My AI Clone", page_icon="🤖")
st.title("🤖 My AI Clone")
st.write("I am an AI assistant based on your document. Ask me anything!")

# --- Core Logic ---
@st.cache_resource
def get_vectorstore_from_pdf(pdf_path):
    """Loads a PDF, splits it into chunks, and creates a vector store."""
    if not os.path.exists(pdf_path):
        st.error(f"Error: The file '{pdf_path}' was not found. Please make sure it's in the 'data' folder.")
        return None

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    document_chunks = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(document_chunks, embeddings)
    return vector_store

def get_context_retriever_chain(vector_store):
    """Creates a retrieval chain using the Llama 3 model via Groq."""
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.2)
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based only on the provided context:\n\n{context}"),
        ("user", "{input}"),
    ])
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, stuff_documents_chain)

# --- Session State Management & Main Flow ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Hello! How can I help you today?")]

# IMPORTANT: Change 'knowledge.pdf' to the actual name of your PDF file
data_path = "data/resume.pdf" 

vector_store = get_vectorstore_from_pdf(data_path)

if vector_store:
    retriever_chain = get_context_retriever_chain(vector_store)

    user_query = st.chat_input("Type your message here...")
    if user_query:
        response = retriever_chain.invoke({"input": user_query, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response['answer']))

    # Display conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)