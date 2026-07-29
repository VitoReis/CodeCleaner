import math
import os
import statistics
from pathlib import Path

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import TokenTextSplitter

from config import (
    DATA_DIR,
    PERSIST_DIR,
    embed_model,
)
from embeddings import embed_texts_parallel


def load_existing_index():
    storage = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage)
    return index


def read_documents(data_dir):
    docs = SimpleDirectoryReader(data_dir).load_data(
        num_workers=min(4, os.cpu_count() or 1)
    )
    if not docs:
        raise Exception("No documents found")
    total_chars = sum(len(doc.text) for doc in docs)
    print(f"Documents: {len(docs)}")
    print(f"Characters: {total_chars:,}")
    estimated = math.ceil(total_chars / (Settings.chunk_size - Settings.chunk_overlap))
    print(f"Chunk estimate: {estimated:,}")
    return docs


def create_nodes(documents):
    splitter = TokenTextSplitter(
        chunk_size=Settings.chunk_size,
        chunk_overlap=Settings.chunk_overlap,
    )
    nodes = splitter.get_nodes_from_documents(documents)
    sizes = [len(n.text) for n in nodes]
    print(f"Chunks: {len(nodes):,}")
    print(f"Smaller: {min(sizes):,}")
    print(f"Bigger: {max(sizes):,}")
    print(f"Average: {statistics.mean(sizes):.0f}")
    return nodes


def generate_embeddings(nodes):
    texts = [n.get_content() for n in nodes]
    embeddings = embed_texts_parallel(texts)
    for node, embedding in zip(nodes, embeddings):
        node.embedding = embedding


def build_index(nodes):
    index = VectorStoreIndex(
        nodes,
        embed_model=embed_model,
        show_progress=True,
    )
    return index


def save_index(index):
    index.storage_context.persist(persist_dir=PERSIST_DIR)


def load_and_index_documents(data_dir=DATA_DIR):
    if Path(PERSIST_DIR).exists():
        return load_existing_index()
    docs = read_documents(data_dir)
    nodes = create_nodes(docs)
    generate_embeddings(nodes)
    index = build_index(nodes)
    save_index(index)
    return index
