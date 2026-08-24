import subprocess
from indexer import load_and_index_documents
from llama_index.llms.ollama import Ollama
from translations import translate


def create_query_engine(index, model_name):
    if model_name:
        llm = Ollama(model=model_name, request_timeout=300)
        retriever = index.as_retriever(similarity_top_k=2)
        return retriever, llm


def send_code(code, model_name):
    index = load_and_index_documents()
    retriever, llm = create_query_engine(index, model_name)
    nodes = retriever.retrieve(code)
    context = "\n".join(n.text for n in nodes if n.score and n.score > 0.75)
    prompt = f"{code}\n\n({translate("best_practice_reference")}:\n{context})"
    print(context)
    reply = llm.complete(prompt)
    return str(reply)


def create_model(model_name):
    try:
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", "Modelfile"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        return {
            "success": True,
            "message": result.stdout or "Modelo criado com sucesso.",
        }
    except subprocess.CalledProcessError as error:
        return {"success": False, "message": error.stderr or str(error)}
    except FileNotFoundError:
        return {
            "success": False,
            "message": "O Ollama não foi encontrado. Verifique se ele está instalado e disponível no PATH.",
        }


def get_ollama_models():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        lines = result.stdout.strip().splitlines()
        models = []
        for line in lines[1:]:
            parts = line.split()

            if parts:
                models.append(parts[0])
        return models
    except Exception as error:
        print(f"Erro ao buscar modelos do Ollama: {error}")
        return []
