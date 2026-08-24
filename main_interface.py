import customtkinter as ctk
import threading

from llm_service import send_code, get_ollama_models
from translations import (
    get_available_languages,
    get_current_language,
    translate,
    change_language,
)


def create_main_interface(master, show_main_screen, show_modelfile_screen):
    frame = ctk.CTkFrame(master)

    loading_job = None
    loading_counter = 0

    # MAIN LAYOUT
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=0)

    # HEADER
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
    header_frame.grid_columnconfigure(0, weight=1)

    # TITLE
    title_label = ctk.CTkLabel(
        header_frame, text=translate("welcome_message"), font=("Arial", 16)
    )
    title_label.grid(row=0, column=0, sticky="w")

    # LANGUAGES
    languages = get_available_languages()
    selected_language = ctk.StringVar(value=get_current_language())

    def on_language_change(new_language):
        change_language(new_language)
        show_main_screen()

    language_dropdown = ctk.CTkOptionMenu(
        header_frame,
        values=languages,
        variable=selected_language,
        width=120,
        command=on_language_change,
    )
    language_dropdown.grid(row=0, column=1, sticky="e")

    # CHAT BOX
    chatbox = ctk.CTkTextbox(frame, state="disabled", wrap="word")
    chatbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(20, 10))
    chatbox.tag_config("separator", justify="center")
    chatbox.tag_config("assistant", justify="left", lmargin1=10, lmargin2=10)
    chatbox.tag_config("user", justify="left", lmargin1=10, lmargin2=10)

    # BOTTOM FRAME
    bottom_frame = ctk.CTkFrame(frame)
    input_box = ctk.CTkTextbox(bottom_frame, height=80)

    # OLLAMA MODELS
    ollama_models = get_ollama_models()
    if not ollama_models:
        ollama_models = [translate("no_ollama_models_found")]
    selected_model = ctk.StringVar(value=ollama_models[0])
    model_dropdown = ctk.CTkOptionMenu(
        bottom_frame, values=ollama_models, variable=selected_model, width=160
    )

    # CREATE MODEL
    create_model_button = ctk.CTkButton(
        bottom_frame,
        text=translate("create_model"),
        width=120,
        command=show_modelfile_screen,
    )

    # LOADING LABEL
    loading_label = ctk.CTkLabel(
        bottom_frame, text=translate("loading"), font=("Arial", 16)
    )

    # CHAT
    def insert_chatbox(text, sender):
        chatbox.configure(state="normal")
        if sender == "user":
            chatbox.insert(
                "end",
                f"{translate('user')}\n",
                "separator",
            )
            chatbox.insert("end", text + "\n\n", "user")
        else:
            chatbox.insert(
                "end",
                f"{translate('assistant')}\n",
                "separator",
            )
            chatbox.insert("end", text + "\n\n", "assistant")
        chatbox.see("end")
        chatbox.configure(state="disabled")

    # BOTTOM FRAME
    def insert_bottom_frame_components():
        bottom_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=0)
        bottom_frame.grid_columnconfigure(2, weight=0)
        bottom_frame.grid_columnconfigure(3, weight=0)
        input_box.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
        model_dropdown.grid(row=2, column=1, padx=(0, 5), pady=10)
        create_model_button.grid(row=2, column=2, padx=5, pady=10)
        button.grid(row=2, column=3, padx=(5, 10), pady=10)

    # LOADING ANIMATION
    def animate_loading():
        nonlocal loading_counter, loading_job
        dots = "." * ((loading_counter % 3) + 1)
        loading_label.configure(text=f"{translate('loading')}{dots}")
        loading_counter += 1
        loading_job = frame.after(500, animate_loading)

    def loading_animation(enable):
        nonlocal loading_job, loading_counter
        if enable:
            input_box.grid_forget()
            model_dropdown.grid_forget()
            create_model_button.grid_forget()
            button.grid_forget()
            create_model_button.configure(state="disabled")
            language_dropdown.configure(state="disabled")
            loading_label.grid(row=1, column=0, columnspan=3, pady=20)
            loading_counter = 0
            animate_loading()
        else:
            if loading_job is not None:
                frame.after_cancel(loading_job)
                loading_job = None
            loading_label.grid_forget()
            language_dropdown.configure(state="enable")
            create_model_button.configure(state="normal")
            insert_bottom_frame_components()

    # AI REQUEST
    def finish_request(reply):
        insert_chatbox(reply, "assistant")
        loading_animation(False)

    def worker(code, model_name):
        try:
            reply = send_code(code, model_name)
            frame.after(0, lambda: finish_request(reply))
        except Exception as error:
            error_message = str(error)
            frame.after(
                0,
                lambda: finish_request(
                    f"{translate('error_processing_code')}: {error_message}"
                ),
            )

    def send_button_callback():
        code = input_box.get("1.0", "end").strip()
        if not code:
            return
        model_name = selected_model.get()
        if model_name == translate("no_ollama_models_found"):
            insert_chatbox(translate("no_ollama_models_found"), "assistant")
            return
        insert_chatbox(code, "user")
        input_box.delete("1.0", "end")
        loading_animation(True)
        threading.Thread(target=worker, args=(code, model_name), daemon=True).start()

    # SEND BUTTON
    button = ctk.CTkButton(
        bottom_frame, text=translate("send"), width=120, command=send_button_callback
    )
    insert_bottom_frame_components()
    return frame
