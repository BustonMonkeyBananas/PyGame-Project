import tkinter as tk
from tkinter import ttk, StringVar

from languages import languages

volume = 50
language = "Russian"
difficult = "Лёгкая"


def settings():
    global volume, language, difficult
    wind = tk.Tk()
    wind.geometry("624x312")
    wind.title("Настройки")
    wind["bg"] = "#1e1f22"

    canvas = tk.Canvas(height=312, width=624, bg="#1e1f22")
    canvas.pack(expand=1)

    canvas.create_text(116, 58, text="Сложность", justify="center", fill="#FFFFFF")
    difficulties = ["Лёгкая", "Средняя", "Высокая"]
    base = StringVar(value=difficult)

    easy = ttk.Radiobutton(text=difficulties[0], value=difficulties[0], variable=base)
    canvas.create_window(116, 80, window=easy)

    mid = ttk.Radiobutton(text=difficulties[1], value=difficulties[1], variable=base)
    canvas.create_window(116, 105, window=mid)


    diff = ttk.Radiobutton(text=difficulties[2], value=difficulties[2], variable=base)
    canvas.create_window(116, 130, window=diff)
    difficult = base

    canvas.create_text(312, 58, text="Язык", justify="center", fill="#FFFFFF")
    langs = [i[1] for i in languages]
    lang_var = StringVar(value=langs[langs.index(language)])
    list_languages = ttk.Combobox(values=langs,
                                  textvariable=lang_var)
    canvas.create_window(312, 80, window=list_languages)
    language = list_languages.get()

    canvas.create_text(520, 58, text="Громкость", justify="center", fill="#FFFFFF")
    vol = ttk.Scale(wind, from_=0, to=100, orient="vertical", value=50)
    canvas.create_window(520, 170, height=200, window=vol)
    volume = vol.get()

    wind.mainloop()