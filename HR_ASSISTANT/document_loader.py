from langchain_community.document_loaders import TextLoader
from HR_ASSISTANT import config

def load_document(file_path: str = config.DATA_FILE_PATH):
    loader = TextLoader(file_path, encoding= 'utf-8')
    documents = loader.load()
    return documents