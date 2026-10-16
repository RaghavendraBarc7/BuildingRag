from HR_ASSISTANT import config 
from HR_ASSISTANT.agent import create_hr_agent
from HR_ASSISTANT.document_loader import load_document
from HR_ASSISTANT.llm import get_llm
from HR_ASSISTANT.splitter import split_into_chunks
from HR_ASSISTANT.tools import create_search_tool
from HR_ASSISTANT.vector_store import(
    build_vector_store, 
    get_retriever, 
    load_vector_store, 
    save_vector_store, 
    vector_store_exists,
)

def build_vector_store_for_documents(file_path: str = config.DATA_FILE_PATH):
    """LOAD+SPLIT+EMBED the document, reusing a saved index if we have one"""
    if vector_store_exists():
        print("Found a saved vector store on disk, loading it (fast, no re-embedding).")
        return load_vector_store()
    
    print("No saved vector store found, building one from scratch.")
    documents = load_document(file_path)
    chunks = split_into_chunks(documents)
    print(f"Loaded '{file_path}' and split it into {len(chunks)} chunks.")
    
    vector_store = build_vector_store(chunks)
    save_vector_store(vector_store)
    print("Vector store built and saved to disk for next time.")
    return vector_store

def build_hr_assistant(file_path: str = config.DATA_FILE_PATH):
    """Build the full RAG agent, ready to answer questions."""
    config.check_api_keys()
    
    vector_store = build_vector_store_for_documents(file_path)
    retriever = get_retriever(vector_store)
    search_tool = create_search_tool(retriever)
    
    llm = get_llm()
    agent = create_hr_agent(llm, [search_tool])
    
    return agent

def ask(agent, question: str) -> str:
    """Ask the agent a question and return its final answer as plain text."""
    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return response["messages"][-1].text