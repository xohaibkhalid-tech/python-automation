import tkinter as tk
from tkinter import messagebox
import openpyxl
import csv
import os
from datetime import date

WORKERS_FILE = "workers.txt"
ATT_FILE = "attendance.csv"
TODAY = str(date.today())
TODAY_PRETTY = date.today().strftime("%d %B %Y")

workers = []
if os.path.exists(WORKERS_FILE):
    with open(WORKERS_FILE, encoding="utf-8") as f:
        workers = [l.strip() for l in f if l.strip()]

def save_workers():
    with open(WORKERS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(workers))

def refresh_list():
    worker_list.delete(0, tk.END)
    for w in workers:
        worker_list.insert(tk.END, w)

def add_worker():
    name = worker_entry.get().strip()
    if not name:
        messagebox.showwarning("Khaali!", "Naam likho!")
        return
    if name in workers:
        messagebox.showwarning("Hai!", "Ye naam pehle se hai!")
        return
    workers.append(name)
    save_workers()
    refresh_list()
    worker_entry.delete(0, tk.END)
    messagebox.showinfo("Ho gaya!", name + " add ho gaya!")

def mark(status):
    sel = worker_list.curselection()
    if not sel:
        messagebox.showwarning("Select karo!", "Pehle worker select karo!")
        return
    name = workers[sel[0]]
    if os.path.exists(ATT_FILE):
        with open(ATT_FILE, encoding="utf-8") as f:
            for row in csv.reader(f):
                if len(row) >= 2 and row[0] == TODAY and row[1] == name:
                    messagebox.showinfo("Ho gaya!", name + " ki hazri lag chuki!")
                    return
    with open(ATT_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([TODAY, name, status])
    messagebox.showinfo("Ho gaya!", name + ": " + status + " (" + TODAY_PRETTY + ")")

def make_report():
    if not os.path.exists(ATT_FILE):
        messagebox.showwarning("Khaali!", "Koi hazri nahi lagi abhi!")
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append(["Date", "Worker", "Status"])
    with open(ATT_FILE, encoding="utf-8") as f:
        for row in csv.reader(f):
            ws.append(row)
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 12
    fname = "attendance_report.xlsx"
    wb.save(fname)
    messagebox.showinfo("Ho gaya!", "Report ban gayi: " + fname)

root = tk.Tk()
root.title("Attendance Register")
root.geometry("450x580")

tk.Label(root, text="Attendance Register", font=("Arial", 18, "bold")).pack(pady=(15, 2))
tk.Label(root, text="Date: " + TODAY_PRETTY, font=("Arial", 13, "bold"),
         fg="#1565C0").pack(pady=(0, 8))

frame = tk.Frame(root)
frame.pack(pady=5)
tk.Label(frame, text="Worker ka naam:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
worker_entry = tk.Entry(frame, font=("Arial", 12), width=20)
worker_entry.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Add Worker", font=("Arial", 11, "bold"),
          command=add_worker,
          bg="#1565C0", fg="white", padx=10, pady=5).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Workers:", font=("Arial", 12, "bold")).pack(pady=(15, 5))
worker_list = tk.Listbox(root, font=("Arial", 12), width=35, height=8)
worker_list.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="HAZIR", font=("Arial", 14, "bold"),
          command=lambda: mark("Hazir"),
          bg="#2E7D32", fg="white", padx=25, pady=10).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="CHHUTTI", font=("Arial", 14, "bold"),
          command=lambda: mark("Chhutti"),
          bg="#C62828", fg="white", padx=25, pady=10).pack(side=tk.LEFT, padx=10)

tk.Button(root, text="Monthly Report (Excel)", font=("Arial", 12, "bold"),
          command=make_report,
          bg="#EF6C00", fg="white", padx=20, pady=10).pack(pady=15)

refresh_list()
root.mainloop()
