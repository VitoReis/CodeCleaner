import logging
import os

from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding

logging.basicConfig(level=logging.INFO)

DATA_DIR = "data"
PERSIST_DIR = "./storage"

EMBED_MODEL_NAME = "nomic-embed-text"
EMBED_TEXT_INSTRUCTION = "search_document:"
EMBED_QUERY_INSTRUCTION = "search_query:"

Settings.chunk_size = 1024
Settings.chunk_overlap = 100

EMBED_BATCH_SIZE = int(os.environ.get("EMBED_BATCH_SIZE", 10))

embed_model = OllamaEmbedding(
    model_name=EMBED_MODEL_NAME,
    text_instruction=EMBED_TEXT_INSTRUCTION,
    query_instruction=EMBED_QUERY_INSTRUCTION,
    embed_batch_size=EMBED_BATCH_SIZE,
    client_kwargs={"timeout": None},
)
Settings.embed_model = embed_model
