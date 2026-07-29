from config import llm


def create_query_engine(index):
    return index.as_query_engine(
        llm=llm,
        similarity_top_k=5,
        response_mode="compact",
    )
