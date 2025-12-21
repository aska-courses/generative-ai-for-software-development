
import os
from dotenv import load_dotenv

EMBEDDING_MODEL = "text-embedding-3-small" 
CHAT_MODEL = "gpt-4o-mini"               
DB_DIR = "vector_db"
DB_DIR_OVERLAP = "vector_db_overlap"
KNOWLEDGE_BASE_DIR = "knowledge-base"
EVAL_FILE = 'eval_queries.jsonl'

# Load .env with OPENAI_API_KEY
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in your environment/.env")
os.environ["OPENAI_API_KEY"] = api_key
