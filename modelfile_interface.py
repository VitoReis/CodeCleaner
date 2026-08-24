import textwrap

import customtkinter as ctk

from llm_service import create_model
from translations import translate


def create_modelfile_interface(master, show_main_screen):
    frame = ctk.CTkFrame(master)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    # TITLE
    title_label = ctk.CTkLabel(
        frame, text=translate("create_local_model"), font=("Arial", 24)
    )
    title_label.grid(row=0, column=0, pady=(20, 10))

    # SCROLL AREA
    scroll_frame = ctk.CTkScrollableFrame(frame)
    scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
    scroll_frame.grid_columnconfigure(1, weight=1)

    # NEW MODEL NAME
    ctk.CTkLabel(scroll_frame, text=translate("new_model_name")).grid(
        row=0, column=0, sticky="w", padx=10, pady=10
    )

    new_model_entry = ctk.CTkEntry(scroll_frame)
    new_model_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
    new_model_entry.insert(0, "code-cleaner")

    # BASE MODEL
    ctk.CTkLabel(scroll_frame, text=translate("base_model_name")).grid(
        row=1, column=0, sticky="w", padx=10, pady=10
    )
    model_entry = ctk.CTkEntry(scroll_frame)
    model_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
    model_entry.insert(0, "llama3")

    # SYSTEM MESSAGE
    ctk.CTkLabel(scroll_frame, text=translate("modelfile")).grid(
        row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5)
    )
    system_textbox = ctk.CTkTextbox(scroll_frame, height=120)
    system_textbox.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    system_textbox.insert(
        "1.0",
        translate("modelfile_example"),
    )

    # PARAMETERS
    parameters = [
        ("num_ctx", "parameter_context", "4096"),
        ("seed", "parameter_randomness", "42"),
        ("temperature", "parameter_creativity", "0.1"),
        ("top_k", "parameter_variety", "20"),
        ("top_p", "parameter_diversity", "0.8"),
        ("repeat_penalty", "parameter_repetition", "1.1"),
        ("num_predict", "parameter_max_output", "2048"),
    ]
    parameter_entries = {}
    for row, (parameter_name, translation_key, default_value) in enumerate(
        parameters, start=4
    ):
        ctk.CTkLabel(scroll_frame, text=translate(translation_key)).grid(
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
            status_label.configure(text=translate("base_model_required"))
            return
        parameter_values = {
            name: entry.get() for name, entry in parameter_entries.items()
        }
        content = (
            f"FROM {base_model}\n\n"
            f'SYSTEM """\n'
            f"{system_message}\n"
            f'"""\n\n'
            f'PARAMETER num_ctx {parameter_values["num_ctx"]}\n'
            f'PARAMETER seed {parameter_values["seed"]}\n\n'
            f'PARAMETER temperature {parameter_values["temperature"]}\n'
            f'PARAMETER top_k {parameter_values["top_k"]}\n'
            f'PARAMETER top_p {parameter_values["top_p"]}\n'
            f'PARAMETER repeat_penalty {parameter_values["repeat_penalty"]}\n\n'
            f'PARAMETER num_predict {parameter_values["num_predict"]}\n'
            f'PARAMETER stop "<|im_end|>"\n'
            f'PARAMETER stop "<|im_start|>"\n'
        )
        try:
            with open("Modelfile", "w", encoding="utf-8") as file:
                file.write(content)
            status_label.configure(text=translate("modelfile_created_successfully"))
            status_label.configure(text=translate("creating_model_ollama"))
            frame.update_idletasks()
            response = create_model(new_model_name)
            if response["success"]:
                status_label.configure(
                    text=translate(f"model_created_successfully_with_name").format(
                        model_name=new_model_name
                    )
                )
            else:
                status_label.configure(
                    text=translate("error_creating_model").format(
                        message=response["message"]
                    )
                )
        except Exception as error:
            status_label.configure(
                text=translate("error_creating_modelfile").format(error=error)
            )

    # BUTTONS
    buttons_frame = ctk.CTkFrame(frame)
    buttons_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    back_button = ctk.CTkButton(
        buttons_frame, text=translate("back"), command=show_main_screen
    )
    back_button.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    create_button = ctk.CTkButton(
        buttons_frame, text=translate("create_model"), command=save_modelfile
    )
    create_button.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
    return frame
