import customtkinter as ctk
from llm_service import create_model


def create_modelfile_interface(master, show_main_screen):
    frame = ctk.CTkFrame(master)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    # TITLE
    title_label = ctk.CTkLabel(
        frame, text="Criar novo modelo local", font=("Arial", 24)
    )
    title_label.grid(row=0, column=0, pady=(20, 10))

    # SCROLL AREA
    scroll_frame = ctk.CTkScrollableFrame(frame)
    scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
    scroll_frame.grid_columnconfigure(1, weight=1)

    # NEW MODEL NAME
    ctk.CTkLabel(scroll_frame, text="Nome do novo modelo:").grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )
    new_model_entry = ctk.CTkEntry(scroll_frame)
    new_model_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
    new_model_entry.insert(0, "code-cleaner")

    # BASE MODEL
    ctk.CTkLabel(scroll_frame, text="Nome do modelo base:").grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    model_entry = ctk.CTkEntry(scroll_frame)
    model_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
    model_entry.insert(0, "llama3.1")

    # SYSTEM MESSAGE
    ctk.CTkLabel(scroll_frame, text="Modelfile:").grid(
        row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5)
    )
    system_textbox = ctk.CTkTextbox(scroll_frame, height=120)
    system_textbox.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    system_textbox.insert(
        "1.0",
        "Você é um especialista em refatoração de código.\n"
        "Objetivo:\n"
        "Receber código fonte e retornar uma versão mais legível.\n"
        "Regras:\n"
        "- Nunca altere a lógica.\n"
        "- Nunca remova funcionalidades.\n"
        "- Preserve compatibilidade.\n"
        "- Melhore identação.\n"
        "- Organize imports.\n"
        "- Renomeie variáveis locais quando isso aumentar a clareza.\n"
        "- Retorne apenas o código.\n"
        "- Responda apenas com o código, sem explicações.\n",
    )

    # PARAMETERS
    parameters = [
        ("num_ctx (Contexto)", "4096"),
        ("seed (Aleatoriedade)", "42"),
        ("temperature (Criatividade)", "0.7"),
        ("top_k (Variedade)", "40"),
        ("top_p (Diversidade)", "0.9"),
        ("repeat_penalty (Repetição)", "1.1"),
        ("num_predict (Saída máxima)", "2048"),
    ]
    parameter_entries = {}
    for row, (parameter_name, default_value) in enumerate(parameters, start=4):
        ctk.CTkLabel(scroll_frame, text=parameter_name).grid(
            row=row, column=0, sticky="w", padx=10, pady=5
        )
        entry = ctk.CTkEntry(scroll_frame)
        entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        entry.insert(0, default_value)
        parameter_entries[parameter_name] = entry

    # STATUS
    status_label = ctk.CTkLabel(scroll_frame, text="")
    status_label.grid(row=11, column=0, columnspan=2, pady=10)

    # GENERATE MODELFILE
    def save_modelfile():
        base_model = model_entry.get().strip()
        new_model_name = new_model_entry.get().strip()
        system_message = system_textbox.get("1.0", "end").strip()
        if not base_model:
            status_label.configure(text="Informe o modelo base.")
            return
        parameter_values = {
            name: entry.get() for name, entry in parameter_entries.items()
        }
        content = f'''# ======================================
# = MODELFILE GERADO PELO CODE CLEANER =
# ======================================

# Modelo Base
FROM {base_model}

# Mensagem do Sistema
SYSTEM """
{system_message}
"""

# Parâmetros de Performance e Memória
PARAMETER num_ctx {parameter_values["num_ctx (Contexto)"]}
PARAMETER seed {parameter_values["seed (Aleatoriedade)"]}

# Parâmetros de Criatividade e Amostragem
PARAMETER temperature {parameter_values["temperature (Criatividade)"]}
PARAMETER top_k {parameter_values["top_k (Variedade)"]}
PARAMETER top_p {parameter_values["top_p (Diversidade)"]}
PARAMETER repeat_penalty {parameter_values["repeat_penalty (Repetição)"]}

# Limites de Saída
PARAMETER num_predict {parameter_values["num_predict (Saída máxima)"]}
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|im_start|>"
'''
        try:
            with open("Modelfile", "w", encoding="utf-8") as file:
                file.write(content)
            status_label.configure(text="Modelfile criado com sucesso.")
            status_label.configure(text="Criando modelo no Ollama...")
            frame.update_idletasks()
            response = create_model(new_model_name)
            if response["success"]:
                status_label.configure(
                    text=f"Modelo '{new_model_name}' criado com sucesso."
                )
            else:
                status_label.configure(
                    text=f"Erro ao criar modelo: {response['message']}"
                )
        except Exception as error:
            status_label.configure(text=f"Erro ao criar Modelfile: {error}")

    # BUTTONS
    buttons_frame = ctk.CTkFrame(frame)
    buttons_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    back_button = ctk.CTkButton(buttons_frame, text="Voltar", command=show_main_screen)
    back_button.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    create_button = ctk.CTkButton(
        buttons_frame, text="Criar Modelo", command=save_modelfile
    )
    create_button.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
    return frame
