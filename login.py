import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

name = ""
skin = 0
password = ""
con = sqlite3.connect("grangegrad.sqlite")
cur = con.cursor()
sql = '''SELECT loged FROM game'''

wind = tk.Tk()
wind.geometry("624x312")
wind.title("Вход/Регистрация")
wind["bg"] = "#1e1f22"
wind.clipboard_clear()
canvas = tk.Canvas(height=312, width=624, bg="#1e1f22")
canvas.pack(expand=1)

def done():
    messagebox.showinfo("Вы зарегистрированы!", "Вы зарегистрированы!")
    wind.destroy()
    new_sql = f'''INSERT INTO accounts (name, password, skin, difficulty, language, volume, level) VALUES ({name}, {password}, {skin}, 1, 'Russian', 50, 0)'''
    cur.execute(new_sql)
    con.commit()
    cur.execute('''UPDATE game SET loged = 1''')
    con.commit()

def sign():
    if (name, ) in cur.execute('''SELECT name FROM accounts'''):
        messagebox.showinfo("Вы Вошли!", "Вы вошли!")
        wind.destroy()
        cur.execute('''UPDATE game SET loged = 1''')
        con.commit()
    else:
        messagebox.showinfo("Неверное имя или пароль!", "Неверное имя или пароль!")

def registration():
    global name, password, skin
    canvas.destroy()
    regcan = tk.Canvas(height=312, width=624, bg="#1e1f22")
    regcan.pack()
    regcan.create_text(312, 20, text="Регистрация", justify="center", fill="red", font="Elephant 20")

    name_line = tk.Entry(wind, width=50)
    password_line = tk.Entry(wind, width=50)
    password_again = tk.Entry(wind, width=50)

    regcan.create_text(312, 70, text="имя", justify="center", fill="white")
    regcan.create_window(312, 90, window=name_line)

    regcan.create_text(312, 110, text="придумайте пароль", justify="center", fill="white")
    regcan.create_window(312, 130, window=password_line)

    regcan.create_text(312, 150, text="повторите пароль", justify="center", fill="white")
    regcan.create_window(312, 170, window=password_again)

    done_btn = ttk.Button(text="Войти")
    regcan.create_window(312, 250, window=done_btn)
    name, password, skin = name_line.get(), password_line.get(), 0
    done_btn.configure(command=sign)

def sign_in():
    global name, password
    canvas.destroy()
    sigcan = tk.Canvas(height=312, width=624, bg="#1e1f22")
    sigcan.pack()
    sigcan.create_text(312, 20, text="Регистрация", justify="center", fill="red", font="Elephant 20")

    name_line = tk.Entry(wind, width=50)
    password_line = tk.Entry(wind, width=50)

    sigcan.create_text(312, 90, text="имя", justify="center", fill="white")
    sigcan.create_window(312, 110, window=name_line)

    sigcan.create_text(312, 130, text="пароль", justify="center", fill="white")
    sigcan.create_window(312, 150, window=password_line)

    name, password = name_line.get(), password_line.get()
    done_btn = ttk.Button(text="Войти")
    sigcan.create_window(312, 250, window=done_btn)
    done_btn.configure(command=sign)

def login():
    register = ttk.Button(text="Регистрация", command=registration)
    canvas.create_window(150, 100, height=50, width=100, window=register)

    signin = ttk.Button(text="Вход", command=sign_in)
    canvas.create_window(450, 100, height=50, width=100, window=signin)

    wind.mainloop()