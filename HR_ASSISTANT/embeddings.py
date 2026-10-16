from langchain_community.embeddings import JinaEmbeddings

from HR_ASSISTANT import config 

def get_embeddings_model():
    return JinaEmbeddings(model_name = config.EMBEDDING_MODEL_NAME)