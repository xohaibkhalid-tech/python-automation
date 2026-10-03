import tkinter as tk
from tkinter import messagebox, ttk
import openpyxl
import sqlite3
import os
from datetime import date

DB = "zkfan_stock.db"
TODAY = date.today().strftime("%d-%m-%Y")

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT, material TEXT, type_model TEXT, party TEXT,
    recv_pcs REAL, recv_kg REAL, used_pcs REAL, used_kg REAL,
    damaged_pcs REAL, rem_pcs REAL, rem_kg REAL)""")
conn.commit()

def num(x):
    try:
        return float(x)
    except:
        return 0

def last_remaining(material, type_model):
    cur.execute("SELECT rem_pcs, rem_kg FROM stock WHERE material=? AND type_model=? ORDER BY id DESC LIMIT 1",
                (material, type_model))
    row = cur.fetchone()
    return row if row else (0, 0)

def refresh_tree():
    for r in tree.get_children():
        tree.delete(r)
    cur.execute("SELECT date, material, type_model, party, recv_pcs, recv_kg, used_pcs, used_kg, damaged_pcs, rem_pcs, rem_kg FROM stock ORDER BY id DESC")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

def add_record():
    material = mat_entry.get().strip()
    if not material:
        messagebox.showwarning("Empty!", "Please enter material name!")
        return
    d = date_entry.get().strip() or TODAY
    type_model = type_entry.get().strip()
    party = party_entry.get().strip()
    rpcs, rkg = num(rpcs_entry.get()), num(rkg_entry.get())
    upcs, ukg = num(upcs_entry.get()), num(ukg_entry.get())
    dmg = num(dmg_entry.get())

    prev_pcs, prev_kg = last_remaining(material, type_model)
    rem_pcs = prev_pcs + rpcs - upcs - dmg
    rem_kg = prev_kg + rkg - ukg
    if rem_pcs < 0 or rem_kg < 0:
        messagebox.showwarning("Stock Short!",
            f"Not enough stock! Available: {prev_pcs:,.0f} pcs, {prev_kg:,.1f} kg")
        return

    cur.execute("INSERT INTO stock (date, material, type_model, party, recv_pcs, recv_kg, used_pcs, used_kg, damaged_pcs, rem_pcs, rem_kg) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (d, material, type_model, party, rpcs, rkg, upcs, ukg, dmg, rem_pcs, rem_kg))
    conn.commit()
    refresh_tree()
    for e in (mat_entry, type_entry, party_entry, rpcs_entry, rkg_entry,
              upcs_entry, ukg_entry, dmg_entry):
        e.delete(0, tk.END)
    messagebox.showinfo("Saved!",
        f"Record saved. Remaining: {rem_pcs:,.0f} pcs, {rem_kg:,.1f} kg")

def make_report():
    cur.execute("SELECT date, material, type_model, party, recv_pcs, recv_kg, used_pcs, used_kg, damaged_pcs, rem_pcs, rem_kg FROM stock ORDER BY id")
    rows = cur.fetchall()
    if not rows:
        messagebox.showwarning("Empty!", "No records yet!")
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stock Register"
    ws.append(["Date", "Material", "Type/Model", "Party", "Recv Pcs", "Recv Kg",
               "Used Pcs", "Used Kg", "Damaged Pcs", "Rem Pcs", "Rem Kg"])
    for r in rows:
        ws.append(r)
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 16
    fname = "stock_report.xlsx"
    wb.save(fname)
    messagebox.showinfo("Done!", "Report saved: " + fname)

root = tk.Tk()
root.title("ZK FAN - Basic Stock Register")
root.geometry("950x650")

tk.Label(root, text="Basic Stock Register", font=("Arial", 18, "bold")).pack(pady=12)

f1 = tk.Frame(root)
f1.pack(pady=4)
tk.Label(f1, text="Date:", font=("Arial", 10)).grid(row=0, column=0, padx=4)
date_entry = tk.Entry(f1, font=("Arial", 10), width=14)
date_entry.grid(row=0, column=1, padx=4)
date_entry.insert(0, TODAY)
tk.Label(f1, text="Material Name:", font=("Arial", 10)).grid(row=0, column=2, padx=4)
mat_entry = tk.Entry(f1, font=("Arial", 10), width=20)
mat_entry.grid(row=0, column=3, padx=4)
tk.Label(f1, text="Type/Model:", font=("Arial", 10)).grid(row=0, column=4, padx=4)
type_entry = tk.Entry(f1, font=("Arial", 10), width=16)
type_entry.grid(row=0, column=5, padx=4)
tk.Label(f1, text="Party Name:", font=("Arial", 10)).grid(row=0, column=6, padx=4)
party_entry = tk.Entry(f1, font=("Arial", 10), width=18)
party_entry.grid(row=0, column=7, padx=4)

f2 = tk.Frame(root)
f2.pack(pady=4)
tk.Label(f2, text="Recv Pcs:", font=("Arial", 10)).grid(row=0, column=0, padx=4)
rpcs_entry = tk.Entry(f2, font=("Arial", 10), width=10)
rpcs_entry.grid(row=0, column=1, padx=4)
tk.Label(f2, text="Recv Kg:", font=("Arial", 10)).grid(row=0, column=2, padx=4)
rkg_entry = tk.Entry(f2, font=("Arial", 10), width=10)
rkg_entry.grid(row=0, column=3, padx=4)
tk.Label(f2, text="Used Pcs:", font=("Arial", 10)).grid(row=0, column=4, padx=4)
upcs_entry = tk.Entry(f2, font=("Arial", 10), width=10)
upcs_entry.grid(row=0, column=5, padx=4)
tk.Label(f2, text="Used Kg:", font=("Arial", 10)).grid(row=0, column=6, padx=4)
ukg_entry = tk.Entry(f2, font=("Arial", 10), width=10)
ukg_entry.grid(row=0, column=7, padx=4)
tk.Label(f2, text="Damaged Pcs:", font=("Arial", 10)).grid(row=0, column=8, padx=4)
dmg_entry = tk.Entry(f2, font=("Arial", 10), width=10)
dmg_entry.grid(row=0, column=9, padx=4)

tk.Button(root, text="Add Record", font=("Arial", 12, "bold"),
          command=add_record,
          bg="#1565C0", fg="white", padx=25, pady=8).pack(pady=8)

cols = ("Date", "Material", "Type/Model", "Party", "R.Pcs", "R.Kg",
        "U.Pcs", "U.Kg", "Dmg", "Rem.Pcs", "Rem.Kg")
tree = ttk.Treeview(root, columns=cols, show="headings", height=12)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=80, anchor="center")
tree.column("Material", width=130)
tree.column("Party", width=120)
tree.pack(pady=5, padx=10, fill="x")

tk.Button(root, text="Stock Report (Excel)", font=("Arial", 12, "bold"),
          command=make_report,
          bg="#2E7D32", fg="white", padx=20, pady=10).pack(pady=10)

refresh_tree()
root.mainloop()
