import customtkinter as ctk
from llm_service import send_code
import threading


def insert_chatbox(text, sender):
    chatbox.configure(state="normal")

    if sender == "user":
        chatbox.insert("end", f"Você: {text}\n\n", "user")
    else:
        chatbox.insert("end", f"IA: {text}\n\n", "assistant")

    chatbox.see("end")
    chatbox.configure(state="disabled")


def worker(prompt):
    reply = send_code(prompt)
    app.after(0, lambda: finish_request(reply))


def finish_request(reply):
    insert_chatbox(reply, "assistant")
    loading_animation(False)


def send_button_callback():
    global loading
    code = input_box.get("1.0", "end").strip()

    if not code:
        return

    # INSERT INPUT IN CHATBOX
    insert_chatbox(code, "user")
    input_box.delete("1.0", "end")

    prompt = (
        "DADO O SEGUINTE CÓDIGO EM C, "
        "REFATORE APLICANDO OS PRINCÍPIOS DE CLEAN CODE. "
        "RESPONDA EM PORTUGUÊS E APENAS COM O CÓDIGO:\n\n" + code
    )

    # CREATING THREAD TO WAIT FOR REPLAY
    loading_animation(True)
    threading.Thread(target=worker, args=(prompt,), daemon=True).start()


def insert_bottom_frame_components():
    # BOTTOM FRAME
    bottom_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
    bottom_frame.grid_columnconfigure(0, weight=1)

    # INPUT BOX
    input_box.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady=10)

    # SEND BUTTON
    button.grid(row=1, column=1, padx=(0, 10), pady=10)


def loading_animation(enable):
    global loading_job, loading_counter

    if enable:
        input_box.grid_forget()
        button.grid_forget()

        loading_label.grid(row=1, column=0, columnspan=2, pady=20)
        loading_counter = 0

        def animate():
            global loading_counter, loading_job
            dots = "." * ((loading_counter % 3) + 1)
            loading_label.configure(text=f"IA está pensando{dots}")
            loading_counter += 1
            loading_job = app.after(500, animate)

        animate()
    else:
        if loading_job is not None:
            app.after_cancel(loading_job)
        loading_label.grid_forget()
        insert_bottom_frame_components()


# INTERFACE LAYOUT
app = ctk.CTk()
app.title("Code Cleaner")
app.geometry("800x600")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=0)

# TITLE
title_label = ctk.CTkLabel(app, text="Bem-vindo(a) ao CodeCleaner", font=("Arial", 16))
title_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))

# CHAT BOX
chatbox = ctk.CTkTextbox(app, state="disabled", wrap="word")
chatbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(20, 10))
chatbox.tag_config("assistant", justify="left", lmargin1=10, lmargin2=10)
chatbox.tag_config("user", justify="right", rmargin=10)

# BOTTOM FRAME COMPONENTS
bottom_frame = ctk.CTkFrame(app)
input_box = ctk.CTkTextbox(bottom_frame, height=80)
button = ctk.CTkButton(
    bottom_frame, text="Enviar", width=120, command=send_button_callback
)

# LOADING
loading_label = ctk.CTkLabel(
    bottom_frame, text="A IA está pensando", font=("Arial", 16)
)
loading_job = None
loading_counter = 0

# INSERT
insert_bottom_frame_components()

app.mainloop()
