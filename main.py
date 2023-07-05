import tkinter as tk
from customtkinter import *

# Chamando a janela do aplicativo
class App(CTk):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

        self.main_frame = CTkFrame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

app = App()
app.geometry("400x240") 
app.title("DashMedidor")
app.mainloop()