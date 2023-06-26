import threading
import tkinter as tk
from PIL import ImageTk, Image
from .style import *
from .settings import *
from .EchoTranslate import EchoTranslate


class EchoApp(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)

        self.title("EchoTranslate")
        self.eval("tk::PlaceWindow . center")
        self.iconbitmap("assets/icon.ico")
        self.resizable(False, False)

        self.is_recording = False
        self.status_lock = threading.Lock()

        self.play_back = True
        self.play_back_type = "Echo"

        widgets_holder = tk.Frame(self, bg = APP_BG)
        widgets_holder.pack(anchor = "center",
                            fill = "both",
                            expand = True)
        widgets_holder.columnconfigure(0, weight = 1)

        cog_image = Image.open("assets/cog.png").resize((50, 50))
        cog_image = ImageTk.PhotoImage(cog_image)

        settings = tk.Button(widgets_holder,
                             image = cog_image,
                             bg = APP_BG,
                             relief = "flat",
                             command = lambda: show_settings(self))
        settings.grid(row = 0,
                      column = 2,
                      padx = 5,
                      pady = 5,
                      sticky = "ne")
        
        self.green_circle = Image.open("altAssets/green_circle.png").resize((125, 125))
        self.green_circle = ImageTk.PhotoImage(self.green_circle)

        self.red_circle = Image.open("altAssets/red_circle.png").resize((125, 125))
        self.red_circle = ImageTk.PhotoImage(self.red_circle)

        self.record_button = tk.Button(widgets_holder,
                                       text = "Start\nRecording",
                                       font = ("Arial", 16, "bold"),
                                       image = self.green_circle,
                                       compound = "center",
                                       fg = APP_FG,
                                       bg = APP_BG,
                                       relief = "flat",
                                       command = self.change_echo_stauts)
        self.record_button.grid(row = 0,
                                column = 0, columnspan = 3,
                                pady = 25,
                                sticky = "ns")

        text_holder = tk.Frame(widgets_holder, bg = APP_BG)
        text_holder.grid(row = 1,
                         column = 0, columnspan = 3,
                         pady = 5,
                         sticky = "ew")

        guide_text = tk.Label(text_holder,
                              text = "Recognized Speech:",
                              font = ("Arial", 14),
                              fg = APP_FG,
                              bg = APP_BG)
        guide_text.grid(row = 0,
                        column = 0,
                        sticky = "w")

        self.display_text = tk.Text(text_holder,
                                    font = ("Arial", 14),
                                    fg = APP_FG,
                                    bg = APP_BG,
                                    width = 40,
                                    height = 4,
                                    state = "normal")
        self.display_text.grid(row = 1,
                               column = 0,
                               sticky = "w")
        self.display_text.bind("<Key>", lambda e: "break")

        translated_holder = tk.Frame(widgets_holder, bg = APP_BG)
        translated_holder.grid(row = 2,
                               column = 0, columnspan = 3,
                               pady = 10,
                               sticky = "ew")
        translated_holder.columnconfigure(0, weight = 1)

        guide_translated = tk.Label(translated_holder,
                                    text = "Translated:",
                                    font = ("Arial", 14),
                                    fg = APP_FG,
                                    bg = APP_BG)
        guide_translated.grid(row = 0,
                              column = 0,
                              sticky = "w")

        self.display_translated = tk.Text(translated_holder,
                                          font = ("Arial", 14),
                                          fg = APP_FG,
                                          bg = APP_BG,
                                          width = 40,
                                          height = 4,
                                          state = "normal")
        self.display_translated.grid(row = 1,
                                     column = 0,
                                     sticky = "w")
        self.display_translated.bind("<Key>", lambda e: "break")

        self.mainloop()

    def change_echo_stauts(self) -> None:
        "Flips the status of the app, if it was running it stops, if it wasn't it starts"
        if self.is_recording:
            self.is_recording = False
            self.record_button.configure(text = "Start\nRecording",
                                         image = self.green_circle)

        else:
            self.is_recording = True
            self.record_button.configure(text = "Stop\nRecording",
                                         image = self.red_circle)

            EchoTranslate(self.display_text, self.display_translated, self)
