import tkinter as tk
from .style import *


def show_settings(app) -> None:
    "Displays a popup to allow the user to change the app settings"
    popup = tk.Toplevel(bg = APP_BG)

    popup.title("Settings")
    popup.iconbitmap("altAssets/icon.ico")
    popup.resizable(False, False)

    widgets_holder = tk.Frame(popup, bg = APP_BG)
    widgets_holder.pack(anchor = "center",
                        fill = "both",
                        expand = True)

    header = tk.Label(widgets_holder,
                      text = "Settings:",
                      font = ("Arial", 16, "bold"),
                      fg = APP_FG,
                      bg = APP_BG)
    header.pack(anchor="center",
                padx = 10,
                pady = 10)
    
    will_play_back = tk.BooleanVar(value = app.play_back)
    play_back = tk.Checkbutton(widgets_holder,
                               text = "Play Translated Audio Back",
                               font = ("Arial", 12),
                               variable = will_play_back,
                               fg = APP_FG,
                               activeforeground = APP_FG,
                               bg = APP_BG,
                               activebackground = APP_BG)
    play_back.pack(anchor = "w",
                   pady = 5,
                   padx = 5)

    play_back_type = tk.StringVar(value = app.play_back_type)

    echo_back = tk.Radiobutton(widgets_holder,
                               text = "Echo Audio Back During Recording",
                               font = ("Arial", 12),
                               variable = play_back_type,
                               value = "Echo",
                               fg = APP_FG,
                               activeforeground = APP_FG,
                               bg = APP_BG,
                               activebackground = APP_BG)
    echo_back.pack(anchor = "w",
                   padx = 5)

    replay_back = tk.Radiobutton(widgets_holder,
                                 text = "Play Audio Back After Recording",
                                 font = ("Arial", 12),
                                 variable = play_back_type,
                                 value = "Replay",
                                 fg = APP_FG,
                                 activeforeground = APP_FG,
                                 bg = APP_BG,
                                 activebackground = APP_BG)
    replay_back.pack(anchor = "w",
                     padx = 5)

    if app.play_back_type == "Echo":
        echo_back.select()
    else:
        replay_back.select()

    buttons_holder = tk.Frame(widgets_holder, bg = APP_BG)
    buttons_holder.pack(anchor = "center",
                        pady = 10,
                        padx = 5)

    save = tk.Button(buttons_holder,
                     text = "Save",
                     font = ("Arial", 12),
                     fg = APP_FG,
                     bg = APP_BG,
                     command = lambda: (save_settings(app, will_play_back, play_back_type), popup.destroy()))
    save.pack(side = "left",
              padx = 5)

    cancel = tk.Button(buttons_holder,
                       text = "Cancel",
                       font = ("Arial", 12),
                       fg = APP_FG,
                       bg = APP_BG,
                       command = popup.destroy)
    cancel.pack(side = "left",
                padx = 5)

    popup_position(popup, app)


def save_settings(app, *settings):
    app.play_back = settings[0].get()
    app.play_back_type = settings[1].get()


def popup_position(popup: tk.Toplevel, window: tk.Tk) -> None:
    """Calculates the position of the main window to place the popup in the middle of it"""
    main_x = window.winfo_x()
    main_y = window.winfo_y()
    main_width = window.winfo_width()
    main_height = window.winfo_height()

    popup.update_idletasks()

    toplevel_width = popup.winfo_width()
    toplevel_height = popup.winfo_height()

    toplevel_x = main_x + (main_width - toplevel_width) // 2
    toplevel_y = main_y + (main_height - toplevel_height) // 2

    popup.geometry(f"+{toplevel_x}+{toplevel_y}")
