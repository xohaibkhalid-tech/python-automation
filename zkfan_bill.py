import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from fpdf import FPDF
import os
from datetime import date

items = []
BILLNO_FILE = "zkfan_billno.txt"
TODAY_PRETTY = date.today().strftime("%d-%m-%Y")

BUSINESS = "ZK FAN"
TAGLINE = "Pakistan's first 30 watts AC/DC manufacturer"
ADDRESS = "GT Road, Gujranwala | zkfans.pk"

def next_billno():
    n = 1
    if os.path.exists(BILLNO_FILE):
        try:
            with open(BILLNO_FILE) as f:
                n = int(f.read().strip())
        except:
            n = 1
    with open(BILLNO_FILE, "w") as f:
        f.write(str(n + 1))
    return f"ZF-{n:04d}"

def num(x):
    try:
        return float(x)
    except:
        return 0

def pick_date():
    top = tk.Toplevel(root)
    top.title("Select Date")
    top.geometry("340x400")
    top.transient(root)
    top.grab_set()
    cal = Calendar(top, selectmode="day", date_pattern="dd-MM-yyyy",
                   font=("Arial", 11), headersbackground="#1565C0",
                   headersforeground="white", selectbackground="#2E7D32")
    cal.pack(padx=10, pady=10, fill="both", expand=True)
    def set_it():
        date_entry.delete(0, tk.END)
        date_entry.insert(0, cal.get_date())
        top.destroy()
    tk.Button(top, text="Select Date", font=("Arial", 11, "bold"),
              command=set_it, bg="#1565C0", fg="white",
              padx=20, pady=6).pack(pady=8)
    top.focus_set()
    top.wait_window()

def add_item():
    desc = desc_entry.get().strip()
    rate = num(rate_entry.get())
    qty = num(qty_entry.get())
    if not desc:
        messagebox.showwarning("Empty!", "Please enter description!")
        return
    if rate <= 0 or qty <= 0:
        messagebox.showwarning("Invalid!", "Rate and Qty must be numbers!")
        return
    items.append([desc, rate, qty])
    items_list.insert(tk.END, f"{desc} | {rate:,.0f} x {qty:,.0f} = Rs. {rate*qty:,.0f}")
    desc_entry.delete(0, tk.END)
    rate_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)

def make_bill():
    if not items:
        messagebox.showwarning("Empty!", "Please add items first!")
        return
    customer = cust_entry.get().strip() or "Customer"
    bill_date = date_entry.get().strip() or TODAY_PRETTY
    billno = next_billno()
    old_qty = num(old_qty_entry.get())
    old_rate = num(old_rate_entry.get())
    old_amt = old_qty * old_rate
    discount = num(disc_entry.get())
    received = num(recv_entry.get())
    paytype = pay_combo.get()

    subtotal = sum(r * q for _, r, q in items)
    net = subtotal - discount - old_amt
    balance = net - received

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 15, BUSINESS, ln=True, align="C")
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 8, TAGLINE, ln=True, align="C")
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, ADDRESS, ln=True, align="C")
    pdf.ln(2)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, "INVOICE", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(95, 10, "Bill No: " + billno)
    pdf.cell(95, 10, "Date: " + bill_date, ln=True)
    pdf.cell(0, 10, "Customer: " + customer, ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(90, 10, "Description", border=1)
    pdf.cell(30, 10, "Rate", border=1)
    pdf.cell(25, 10, "Qty", border=1)
    pdf.cell(45, 10, "Amount", border=1, ln=True)
    pdf.set_font("Arial", "", 11)
    for desc, rate, qty in items:
        pdf.cell(90, 10, desc, border=1)
        pdf.cell(30, 10, f"{rate:,.0f}", border=1)
        pdf.cell(25, 10, f"{qty:,.0f}", border=1)
        pdf.cell(45, 10, f"{rate*qty:,.0f}", border=1, ln=True)

    pdf.ln(3)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 9, f"Subtotal: Rs. {subtotal:,.0f}", ln=True, align="R")
    if old_amt > 0:
        pdf.cell(0, 9, f"Old Fan Return ({old_qty:,.0f} x {old_rate:,.0f}): Rs. {old_amt:,.0f}", ln=True, align="R")
    if discount > 0:
        pdf.cell(0, 9, f"Discount: Rs. {discount:,.0f}", ln=True, align="R")
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 11, f"Net Total: Rs. {net:,.0f}", ln=True, align="R")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 9, f"Received ({paytype}): Rs. {received:,.0f}", ln=True, align="R")
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, f"Balance: Rs. {balance:,.0f}", ln=True, align="R")

    filename = billno.replace("-", "_") + ".pdf"
    pdf.output(filename)
    messagebox.showinfo("Success!", "Bill " + billno + " generated: " + filename)

root = tk.Tk()
root.title("ZK FAN - Invoice")
root.geometry("500x780")

tk.Label(root, text="ZK FAN", font=("Arial", 20, "bold")).pack(pady=(12, 0))
tk.Label(root, text="Invoice", font=("Arial", 14)).pack(pady=(0, 8))

tk.Label(root, text="Customer Name:", font=("Arial", 11)).pack()
cust_entry = tk.Entry(root, font=("Arial", 12), width=32)
cust_entry.pack(pady=3)

dframe = tk.Frame(root)
dframe.pack(pady=3)
tk.Label(dframe, text="Bill Date:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
date_entry = tk.Entry(dframe, font=("Arial", 12), width=18)
date_entry.pack(side=tk.LEFT, padx=5)
date_entry.insert(0, TODAY_PRETTY)
tk.Button(dframe, text="Calendar", font=("Arial", 10, "bold"),
          command=pick_date,
          bg="#1565C0", fg="white", padx=8, pady=3).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Items:", font=("Arial", 12, "bold")).pack(pady=(10, 3))
iframe = tk.Frame(root)
iframe.pack(pady=3)
tk.Label(iframe, text="Description", font=("Arial", 10)).grid(row=0, column=0, padx=4)
tk.Label(iframe, text="Rate", font=("Arial", 10)).grid(row=0, column=1, padx=4)
tk.Label(iframe, text="Qty", font=("Arial", 10)).grid(row=0, column=2, padx=4)
desc_entry = tk.Entry(iframe, font=("Arial", 11), width=22)
desc_entry.grid(row=1, column=0, padx=4)
rate_entry = tk.Entry(iframe, font=("Arial", 11), width=10)
rate_entry.grid(row=1, column=1, padx=4)
qty_entry = tk.Entry(iframe, font=("Arial", 11), width=8)
qty_entry.grid(row=1, column=2, padx=4)
tk.Button(iframe, text="Add", font=("Arial", 10, "bold"),
          command=add_item,
          bg="#1565C0", fg="white", padx=10, pady=3).grid(row=1, column=3, padx=4)

items_list = tk.Listbox(root, font=("Arial", 11), width=52, height=5)
items_list.pack(pady=5)

tk.Label(root, text="Old Fan Return:", font=("Arial", 12, "bold")).pack(pady=(8, 3))
oframe = tk.Frame(root)
oframe.pack(pady=3)
tk.Label(oframe, text="Qty", font=("Arial", 10)).grid(row=0, column=0, padx=4)
tk.Label(oframe, text="Rate", font=("Arial", 10)).grid(row=0, column=1, padx=4)
old_qty_entry = tk.Entry(oframe, font=("Arial", 11), width=10)
old_qty_entry.grid(row=1, column=0, padx=4)
old_rate_entry = tk.Entry(oframe, font=("Arial", 11), width=12)
old_rate_entry.grid(row=1, column=1, padx=4)
old_rate_entry.insert(0, "2500")

pframe = tk.Frame(root)
pframe.pack(pady=8)
tk.Label(pframe, text="Discount:", font=("Arial", 11)).grid(row=0, column=0, padx=4)
disc_entry = tk.Entry(pframe, font=("Arial", 11), width=10)
disc_entry.grid(row=0, column=1, padx=4)
disc_entry.insert(0, "0")
tk.Label(pframe, text="Payment:", font=("Arial", 11)).grid(row=0, column=2, padx=4)
pay_combo = ttk.Combobox(pframe, font=("Arial", 11), width=16, state="readonly",
                         values=["Cash", "Bank", "Credit", "Cash on Delivery"])
pay_combo.grid(row=0, column=3, padx=4)
pay_combo.current(0)

rframe = tk.Frame(root)
rframe.pack(pady=5)
tk.Label(rframe, text="Received Amount:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
recv_entry = tk.Entry(rframe, font=("Arial", 12), width=14)
recv_entry.pack(side=tk.LEFT, padx=5)
recv_entry.insert(0, "0")

tk.Button(root, text="Generate Bill (PDF)", font=("Arial", 15, "bold"),
          command=make_bill,
          bg="#2E7D32", fg="white", padx=30, pady=12).pack(pady=15)

root.mainloop()
