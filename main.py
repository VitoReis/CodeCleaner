import customtkinter as ctk
from main_interface import create_main_interface
from modelfile_interface import create_modelfile_interface

app = ctk.CTk()
app.title("Code Cleaner")
app.geometry("800x600")
current_screen = None


def change_screen(screen_function):
    global current_screen
    if current_screen is not None:
        current_screen.destroy()
    current_screen = screen_function(app)
    current_screen.pack(fill="both", expand=True)


def show_main_screen():
    change_screen(lambda master: create_main_interface(master, show_modelfile_screen))


def show_modelfile_screen():
    change_screen(lambda master: create_modelfile_interface(master, show_main_screen))


show_main_screen()
app.mainloop()
