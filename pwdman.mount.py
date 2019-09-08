import tkinter as tk
import tkinter.simpledialog
import sys
import subprocess

encrypted = sys.argv[1]
decrypted = sys.argv[2]

tk.Tk().withdraw()
password = tkinter.simpledialog.askstring("Password", "Enter password:", show='*')

if password:
    subprocess.call(
        "echo -n {} | encfs --stdinpass {} {}".format(password, encrypted, decrypted),
        shell=True
    )
