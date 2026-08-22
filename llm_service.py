import subprocess
from indexer import load_and_index_documents
from query_engine import create_query_engine


def send_code(code, model_name):
    index = load_and_index_documents()
    engine = create_query_engine(index, model_name)
    reply = engine.query(code)
    return reply


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
