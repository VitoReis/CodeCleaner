import json
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
    EMBED_MODEL_NAME,
    EMBED_QUERY_INSTRUCTION,
    EMBED_TEXT_INSTRUCTION,
    PERSIST_DIR,
    embed_model,
)

INDEX_CONFIG_PATH = Path(PERSIST_DIR) / "index_config.json"


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


def build_index(nodes):
    index = VectorStoreIndex(
        nodes,
        embed_model=embed_model,
        show_progress=True,
    )
    return index


def save_index(index):
    index.storage_context.persist(persist_dir=PERSIST_DIR)


def index_config(data_dir):
    data_path = Path(data_dir)
    return {
        "schema_version": 1,
        "data_dir": str(data_path.resolve()),
        "source_files": [
            {
                "path": str(path.relative_to(data_path)),
                "size": path.stat().st_size,
                "modified_ns": path.stat().st_mtime_ns,
            }
            for path in sorted(data_path.rglob("*"))
            if path.is_file()
        ],
        "embedding_model": EMBED_MODEL_NAME,
        "text_instruction": EMBED_TEXT_INSTRUCTION,
        "query_instruction": EMBED_QUERY_INSTRUCTION,
        "chunk_size": Settings.chunk_size,
        "chunk_overlap": Settings.chunk_overlap,
    }


def load_and_index_documents(data_dir=DATA_DIR):
    expected_config = index_config(data_dir)
    if Path(PERSIST_DIR).exists() and INDEX_CONFIG_PATH.exists():
        stored_config = json.loads(INDEX_CONFIG_PATH.read_text(encoding="utf-8"))
        if stored_config == expected_config:
            return load_existing_index()
        print("Embedding configuration changed; rebuilding the persisted index.")
    elif Path(PERSIST_DIR).exists():
        print("Persisted index has no configuration metadata; rebuilding it.")

    docs = read_documents(data_dir)
    nodes = create_nodes(docs)
    index = build_index(nodes)
    save_index(index)
    INDEX_CONFIG_PATH.write_text(
        json.dumps(expected_config, indent=2),
        encoding="utf-8",
    )
    return index
