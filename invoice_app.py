import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF

items = []

def add_item():
    name = item_entry.get().strip()
    if not name:
        messagebox.showwarning("Khaali!", "Item ka naam likho!")
        return
    try:
        qty = int(qty_entry.get())
        price = float(price_entry.get())
    except:
        messagebox.showwarning("Ghalat!", "Qty aur Price number me likho!")
        return
    items.append([name, qty, price])
    items_list.insert(tk.END, f"{name}  x{qty}  = Rs. {qty*price:,.0f}")
    item_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def make_bill():
    if not items:
        messagebox.showwarning("Khaali!", "Pehle items add karo!")
        return
    customer = cust_entry.get().strip() or "Customer"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, "INVOICE", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
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
    messagebox.showinfo("Ho gaya!", "Bill ban gaya: " + filename)

root = tk.Tk()
root.title("Invoice Generator")
root.geometry("450x550")

tk.Label(root, text="Invoice Generator", font=("Arial", 18, "bold")).pack(pady=15)

tk.Label(root, text="Customer Name:", font=("Arial", 11)).pack()
cust_entry = tk.Entry(root, font=("Arial", 12), width=30)
cust_entry.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

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
          bg="#1565C0", fg="white", padx=20, pady=8).pack(pady=10)

items_list = tk.Listbox(root, font=("Arial", 11), width=45, height=8)
items_list.pack(pady=5)

tk.Button(root, text="Bill Banao (PDF)", font=("Arial", 14, "bold"),
          command=make_bill,
          bg="#2E7D32", fg="white", padx=30, pady=12).pack(pady=15)

root.mainloop()
