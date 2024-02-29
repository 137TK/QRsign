import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import Calendar
import pyperclip


import matplotlib.pyplot as plt
import datetime
import sys
from arrange_qr.make_qr import *
import io
import win32clipboard
import cv2
import numpy as np
import configparser
import os


ini_file = "QRsign.ini"

def send_to_clipboard(clip_type, data):
    # クリップボードをクリアして、データをセットする
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def create():
    name = name_entry.get()
    date = datetime.datetime.now().strftime("%Y/%m/%d")
    result = make_qr(make_name_date(name, date), name, date)
    result = np.array(result).tobytes()
    send_to_clipboard(win32clipboard.CF_DIB, result)
    update_ini(name, date)
    messagebox.showinfo("Result", "Function executed successfully!\nresult={}".format(type(result)))


def init_files():
    if(os.path.isfile(".\\config.ini")):
        config_ini = configparser.ConfigParser()
        config_ini.read("config.ini", encoding="utf-8")
        name = config_ini["PreviousInfo"]['Name']
    else:
        name = ""
    return name

def update_ini(name, date):
    config_ini = configparser.ConfigParser()
    config_ini["PreviousInfo"] = { "Name": name,"Date": date }
    with open("config.ini", 'w', encoding='utf-8') as file:
        # 指定したconfigファイルを書き込み
        config_ini.write(file)


# GUIのセットアップ

name = init_files()

root = tk.Tk()
root.title("Input Form")

# 名前入力
name_label = ttk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)
name_entry.insert(0, name)

# 日付選択
date_label = ttk.Label(root, text="Date:")
date_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
date_var = tk.StringVar()
date_entry = ttk.Entry(root, textvariable=date_var, state="readonly")
date_entry.grid(row=1, column=1, padx=5, pady=5)
date_entry.insert(0, datetime.datetime.now().strftime("%Y/%m/%d"))

def choose_date():
    def set_date():
        date_var.set(cal.get_date())
        top.destroy()
    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode="day")
    cal.pack(padx=10, pady=10)
    ttk.Button(top, text="Select", command=set_date).pack(pady=5)

date_button = ttk.Button(root, text="Choose Date", command=choose_date)
date_button.grid(row=1, column=2, padx=5, pady=5)

# # RSAオプション
# rsa_var = tk.BooleanVar()
# rsa_check = ttk.Checkbutton(root, text="RSA Option", variable=rsa_var)
# rsa_check.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

# 送信ボタン
create_button = ttk.Button(root, text="Create !", command=create)
create_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()