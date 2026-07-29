import concurrent.futures

import ollama

from config import (
    EMBED_BATCH_SIZE,
    EMBED_MODEL_NAME,
    MAX_WORKERS,
)

try:
    from tqdm import tqdm
except ImportError:

    def tqdm(iterable, **kwargs):
        return iterable


def batched(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def embed_texts_parallel(
    texts,
    model=EMBED_MODEL_NAME,
    batch_size=EMBED_BATCH_SIZE,
    max_workers=MAX_WORKERS,
):
    client = ollama.Client()
    batches = list(batched(texts, batch_size))
    results = [None] * len(batches)

    def embed_batch(index_and_batch):
        idx, batch = index_and_batch
        resp = client.embed(model=model, input=batch)
        return idx, resp["embeddings"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(embed_batch, (i, batch)) for i, batch in enumerate(batches)
        ]
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Generating embeddings",
        ):
            idx, embeddings = future.result()
            results[idx] = embeddings
    return [emb for batch in results for emb in batch]
