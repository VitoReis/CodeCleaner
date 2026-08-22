import logging
import os

from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding

logging.basicConfig(level=logging.INFO)

DATA_DIR = "data"
PERSIST_DIR = "./storage"

EMBED_MODEL_NAME = "nomic-embed-text"
LLM_MODEL_NAME = "llama3:latest"

Settings.chunk_size = 1024
Settings.chunk_overlap = 100

embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME)

Settings.embed_model = embed_model

MAX_WORKERS = int(os.environ.get("EMBED_MAX_WORKERS", 6))
EMBED_BATCH_SIZE = int(os.environ.get("EMBED_BATCH_SIZE", 32))
