import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os
from datetime import date

items = []
SETTINGS_FILE = "settings.txt"
TODAY_PRETTY = date.today().strftime("%d %B %Y")

def load_settings():
    name, address = "", ""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f]
            if len(lines) > 0:
                name = lines[0]
            if len(lines) > 1:
                address = lines[1]
    return name, address

def save_settings(name, address):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write(name + "\n" + address)

def add_item():
    name = item_entry.get().strip()
    if not name:
        messagebox.showwarning("Empty!", "Please enter an item name!")
        return
    try:
        qty = int(qty_entry.get())
        price = float(price_entry.get())
    except:
        messagebox.showwarning("Invalid!", "Qty and Price must be numbers!")
        return
    items.append([name, qty, price])
    items_list.insert(tk.END, f"{name}  x{qty}  = Rs. {qty*price:,.0f}")
    item_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def make_bill():
    if not items:
        messagebox.showwarning("Empty!", "Please add items first!")
        return
    customer = cust_entry.get().strip() or "Customer"
    business = biz_entry.get().strip()
    address = addr_entry.get().strip()
    bill_date = date_entry.get().strip() or TODAY_PRETTY
    save_settings(business, address)
    if not business:
        business = "INVOICE"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 22)
    pdf.cell(0, 15, business, ln=True, align="C")
    if address:
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, address, ln=True, align="C")
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, "INVOICE", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Date: " + bill_date, ln=True)
    pdf.cell(0, 10, "Customer: " + customer, ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Qty", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(40, 10, "Total", border=1, ln=True)

    pdf.set_font("Arial", "", 12)
    grand = 0
    for name, qty, price in items:
        total = qty * price
        grand += total
        pdf.cell(80, 10, name, border=1)
        pdf.cell(30, 10, str(qty), border=1)
        pdf.cell(40, 10, f"{price:,.0f}", border=1)
        pdf.cell(40, 10, f"{total:,.0f}", border=1, ln=True)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, f"Grand Total: Rs. {grand:,.0f}", ln=True)

    filename = "bill_" + customer.replace(" ", "_") + ".pdf"
    pdf.output(filename)
    messagebox.showinfo("Success!", "Bill generated: " + filename)

root = tk.Tk()
root.title("Invoice Generator")
root.geometry("450x700")

tk.Label(root, text="Invoice Generator", font=("Arial", 18, "bold")).pack(pady=(15, 5))

tk.Label(root, text="Your Business Name:", font=("Arial", 11)).pack()
biz_entry = tk.Entry(root, font=("Arial", 12), width=30)
biz_entry.pack(pady=3)

tk.Label(root, text="Business Address:", font=("Arial", 11)).pack()
addr_entry = tk.Entry(root, font=("Arial", 12), width=30)
addr_entry.pack(pady=3)

saved_name, saved_addr = load_settings()
biz_entry.insert(0, saved_name)
addr_entry.insert(0, saved_addr)

tk.Label(root, text="Customer Name:", font=("Arial", 11)).pack()
cust_entry = tk.Entry(root, font=("Arial", 12), width=30)
cust_entry.pack(pady=3)

tk.Label(root, text="Bill Date:", font=("Arial", 11)).pack()
date_entry = tk.Entry(root, font=("Arial", 12), width=30)
date_entry.pack(pady=3)
date_entry.insert(0, TODAY_PRETTY)

frame = tk.Frame(root)
frame.pack(pady=8)

tk.Label(frame, text="Item", font=("Arial", 11)).grid(row=0, column=0, padx=5)
tk.Label(frame, text="Qty", font=("Arial", 11)).grid(row=0, column=1, padx=5)
tk.Label(frame, text="Price", font=("Arial", 11)).grid(row=0, column=2, padx=5)

item_entry = tk.Entry(frame, font=("Arial", 11), width=18)
item_entry.grid(row=1, column=0, padx=5)
qty_entry = tk.Entry(frame, font=("Arial", 11), width=8)
qty_entry.grid(row=1, column=1, padx=5)
price_entry = tk.Entry(frame, font=("Arial", 11), width=12)
price_entry.grid(row=1, column=2, padx=5)

tk.Button(root, text="Add Item", font=("Arial", 12, "bold"),
          command=add_item,
          bg="#1565C0", fg="white", padx=20, pady=8).pack(pady=8)

items_list = tk.Listbox(root, font=("Arial", 11), width=45, height=5)
items_list.pack(pady=5)

tk.Button(root, text="Generate Bill (PDF)", font=("Arial", 14, "bold"),
          command=make_bill,
          bg="#2E7D32", fg="white", padx=30, pady=12).pack(pady=12)

root.mainloop()
