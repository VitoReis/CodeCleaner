import os
import textwrap

CONFIG_FILE = "./settings.txt"
language = "Português"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split("=", 1)
            if key == "language":
                language = value.strip()
                break


def translate(tag):
    locale = locales[language].get(tag)
    return locale if locale else tag


def get_available_languages():
    return list(locales.keys())


def change_language(new_language):
    global language
    language = new_language
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        for line in lines:
            if line.startswith("language="):
                file.write(f"language={language}\n")
            else:
                file.write(line)


def get_current_language():
    return language


locales = {
    "English": {
        # MAIN INTERFACE
        "create_model": "Create new model",
        "loading": "The AI is thinking",
        "error_processing_code": "Error processing code",
        "no_ollama_models_found": "No Ollama models found.",
        "send": "Send",
        "welcome_message": "Welcome to CodeCleaner",
        "user": "USER",
        "assistant": "ASSISTANT",
        # MODELFILE INTERFACE
        "create_local_model": "Create new local model",
        "new_model_name": "New model name:",
        "base_model_name": "Base model name:",
        "modelfile": "Modelfile:",
        "base_model_required": "Enter the base model.",
        "modelfile_created_successfully": "Modelfile created successfully.",
        "creating_model_ollama": "Creating model in Ollama...",
        "model_created_successfully_with_name": "Model '{model_name}' created successfully.",
        "error_creating_model": "Error creating model: {message}",
        "error_creating_modelfile": "Error creating Modelfile: {error}",
        "back": "Back",
        "create_model": "Create Model",
        "parameter_context": "Context",
        "parameter_randomness": "Randomness",
        "parameter_creativity": "Creativity",
        "parameter_variety": "Variety",
        "parameter_diversity": "Diversity",
        "parameter_repetition": "Repetition",
        "parameter_max_output": "Maximum output",
        "modelfile_example": textwrap.dedent("""
                You are an automatic code refactoring tool.

                Your only task is to receive source code and return the SAME code after applying readability improvements.

                MANDATORY RULES:

                Never explain what was changed.
                Never describe the code.
                Never answer questions about the code.
                Never write text before or after the code.
                Never use Markdown.
                Never use code blocks.
                Never respond in Portuguese.
                Always respond in English when it is necessary to write any text.
                Preserve exactly the logic and behavior of the program.
                Do not remove functionality.
                Do not add functionality.
                Do not change values, conditions, or business rules.
                You may improve local variable names when this increases clarity.
                You may improve indentation and spacing.
                You may organize imports.
                The response must contain ONLY the refactored source code.

                EXAMPLE:

                INPUT:
                def f(a,b):
                x=0
                for i in a:
                if i>10:
                x=x+i
                return x

                OUTPUT:
                def calculate_sum(values, threshold):
                    total = 0
                    for value in values:
                        if value > threshold:
                            total += value
                    return total

                NEVER write explanations.
                NEVER write phrases such as "A function with two arguments...".
                NEVER write "Here is the refactored code".
                NEVER write any text outside the code.
        """).strip(),
        # LLM Service
        "best_practice_reference": "Best practice reference; use only if relevant.",
    },
    "Português": {
        # MAIN INTERFACE
        "create_model": "Criar novo modelo",
        "loading": "A IA está pensando",
        "error_processing_code": "Erro ao processar código",
        "no_ollama_models_found": "Nenhum modelo do Ollama encontrado.",
        "send": "Enviar",
        "welcome_message": "Bem-vindo(a) ao CodeCleaner",
        "user": "VOCÊ",
        "assistant": "ASSISTENTE",
        # MODELFILE INTERFACE
        "create_local_model": "Criar novo modelo local",
        "new_model_name": "Nome do novo modelo:",
        "base_model_name": "Nome do modelo base:",
        "modelfile": "Modelfile:",
        "base_model_required": "Informe o modelo base.",
        "modelfile_created_successfully": "Modelfile criado com sucesso.",
        "creating_model_ollama": "Criando modelo no Ollama...",
        "model_created_successfully_with_name": "Modelo '{model_name}' criado com sucesso.",
        "error_creating_model": "Erro ao criar modelo: {message}",
        "error_creating_modelfile": "Erro ao criar Modelfile: {error}",
        "back": "Voltar",
        "create_model": "Criar Modelo",
        "parameter_context": "Contexto",
        "parameter_randomness": "Aleatoriedade",
        "parameter_creativity": "Criatividade",
        "parameter_variety": "Variedade",
        "parameter_diversity": "Diversidade",
        "parameter_repetition": "Repetição",
        "parameter_max_output": "Saída máxima",
        "modelfile_example": textwrap.dedent("""
            Você é uma ferramenta estrita de refatoração de código C.
            Sua única tarefa é receber código-fonte e devolver o MESMO código após aplicar melhorias de legibilidade baseadas nos princípios de Clean Code.

            REGRAS OBRIGATÓRIAS:
            1. Retorne APENAS o código-fonte refatorado.
            2. NUNCA inclua explicações, introduções, saudações ou conclusões.
            3. NUNCA escreva frases como "Aqui está o código" ou descrições textuais.
            4. NUNCA use blocos de marcação de markdown (como ```c ou ```) se a sua interface não os suportar, ou use apenas o bloco de código puro sem nenhum texto ao redor. (Caso prefira texto puro puro, remova os crases).
            5. Preserve exatamente a lógica, os tipos, os ponteiros e o comportamento do programa original.
            6. Não adicione nem remova funcionalidades de negócio.
            7. Melhore nomes de variáveis locais genéricas (ex: iVar1, iVar2) para nomes semanticamente claros baseados no contexto.
            8. Melhore a indentação, espaçamento e alinhamento.

            EXEMPLO DE ENTRADA:
            int f(int a, int b) {
                int x = 0;
                if (a > 10) {
                    x = a + b;
                }
                return x;
            }

            EXEMPLO DE SAÍDA:
            int calculate_total_value(int initial_value, int increment) {
                int total_result = 0;
                if (initial_value > 10) {
                    total_result = initial_value + increment;
                }
                return total_result;
            }
        """).strip(),
        # LLM Service
        "best_practice_reference": "Referência de boas práticas, use apenas se relevante.",
        "ollama_not_found": "O Ollama não foi encontrado. Verifique se ele está instalado e disponível no PATH.",
        "error_fetching_ollama_models": "Erro ao buscar modelos do Ollama",
        "model_created_successfully_with_name": "Modelo '{model_name}' criado com sucesso.",
    },
}
