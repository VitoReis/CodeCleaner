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
            Você é uma ferramenta automática de refatoração de código.

            Sua única tarefa é receber código-fonte e devolver o MESMO código após aplicar melhorias de legibilidade.

            REGRAS OBRIGATÓRIAS:

            1. Nunca explique o que foi alterado.
            2. Nunca descreva o código.
            3. Nunca responda perguntas sobre o código.
            4. Nunca escreva texto antes ou depois do código.
            5. Nunca use Markdown.
            6. Nunca use blocos de código.
            7. Nunca responda em inglês.
            8. Responda sempre em Português do Brasil quando for necessário escrever algum texto.
            9. Preserve exatamente a lógica e o comportamento do programa.
            10. Não remova funcionalidades.
            11. Não adicione funcionalidades.
            12. Não altere valores, condições ou regras de negócio.
            13. Pode melhorar nomes de variáveis locais quando isso aumentar a clareza.
            14. Pode melhorar indentação e espaçamento.
            15. Pode organizar imports.
            16. A resposta deve conter SOMENTE o código-fonte refatorado.

            EXEMPLO:

            ENTRADA:
            def f(a,b):
            x=0
            for i in a:
            if i>10:
            x=x+i
            return x

            SAÍDA:
            def calculate_sum(values, threshold):
                total = 0
                for value in values:
                    if value > threshold:
                        total += value
                return total

            NUNCA escreva explicações.
            NUNCA escreva frases como "A function with two arguments...".
            NUNCA escreva "Here is the refactored code".
            NUNCA escreva qualquer texto fora do código.
        """).strip(),
    },
}
