import tkinter as tk
from .EchoTranslate import EchoTranslate
import threading


class EchoApp(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)

        self.title("EchoTranslate")
        self.eval("tk::PlaceWindow . center")
        self.geometry("525x400")

        self.is_echoing = False
        self.status_lock = threading.Lock()

        widgets_holder = tk.Frame(self)
        widgets_holder.pack(anchor = "center",
                            fill = "both",
                            expand = True)

        self.echo_button = tk.Button(widgets_holder,
                                     text = "Start\nEchoing",
                                     font = ("Arial", 20, "bold"),
                                     command = self.change_echo_stauts)
        self.echo_button.pack(anchor = "center",
                              pady = 15)

        text_holder = tk.Frame(widgets_holder)
        text_holder.pack(anchor = "center",
                         fill = "x",
                         pady = 5)

        guide_text = tk.Label(text_holder,
                              text = "Input:",
                              font = ("Arial", 14))
        guide_text.grid(row = 0, column = 0)

        self.display_text = tk.Label(text_holder,
                                     font = ("Arial", 14))
        self.display_text.grid(row = 0,
                               column = 1,
                               sticky = "we")

        translated_holder = tk.Frame(widgets_holder)
        translated_holder.pack(anchor = "center",
                         fill = "x",
                         pady = 5)

        guide_translated = tk.Label(translated_holder,
                                    text = "Echo:",
                                    font = ("Arial", 14))
        guide_translated.grid(row = 0, column = 0)

        self.display_translated = tk.Label(translated_holder,
                                           font = ("Arial", 14))
        self.display_translated.grid(row = 0,
                                     column = 1,
                                     sticky = "we")

        self.mainloop()

    def change_echo_stauts(self) -> None:
        if self.is_echoing:
            self.is_echoing = False
            self.echo_button.configure(text = "Start\nEchoing")

        else:
            self.is_echoing = True
            self.echo_button.configure(text = "Stop\nEchoing")

            EchoTranslate(self.display_text, self.display_translated, self)