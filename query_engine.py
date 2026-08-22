from llama_index.llms.ollama import Ollama


def create_query_engine(index, model_name):
    if model_name:
        llm = Ollama(
            model=model_name, request_timeout=300, temperature=0.1, context_window=32768
        )
        return index.as_query_engine(
            llm=llm,
            similarity_top_k=5,
            response_mode="compact",
        )
