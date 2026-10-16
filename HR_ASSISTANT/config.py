import os 
from dotenv import load_dotenv 

load_dotenv()

# ENV VAR 
claude_key = os.getenv('CLAUDE_API_KEY')
jina_key = os.getenv('JINA_API_KEY')


# The project folder (one level above HR_ASSISTANT/), so paths work on any machine
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'HR Policy.txt')

VECTOR_STORE_PATH = os.path.join(PROJECT_ROOT, 'faiss_index')

LLM_MODEL_NAME = "claude-opus-5-5"
EMBEDDING_MODEL_NAME = "jina-embeddings-v3"

# Chunking 
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval Results
TOP_K = 3

# SYSTEM INSTRUCTIONS 

SYSTEM_PROMPT = (
    "YOu are a friendly HR assistant. Always use the search_hr_policy tool to look up "
    "facts before answering. If the answer isn't in the search results, say you don't know instead of guessing."
)

def check_api_keys() -> None:
    if not claude_key:
        raise ValueError("Missing Claude API KEY. Please add it to your config!")
    if not jina_key:
        raise ValueError("Missing JINA API Key. Please add it to your config.")