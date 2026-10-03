import openpyxl

path = "C:/Users/dell/Downloads/Documents/ZK_FAN_Sales_Bills.xlsx"
wb = openpyxl.load_workbook(path)
ws = wb["Sales Bills"]

def num(x):
    return x if isinstance(x, (int, float)) else 0

bills = 0
gross = 0
received = 0
balance = 0

for row in ws.iter_rows(min_row=1, values_only=True):
    if isinstance(row[0], (int, float)):  # sirf asal data rows
        bills += 1
        gross += num(row[7])
        received += num(row[11])
        balance += num(row[12])

print("========== SALES REPORT ==========")
print(f"Total bills: {bills}")
print(f"Total gross: Rs. {gross:,.0f}")
print(f"Total received: Rs. {received:,.0f}")
print(f"Total balance: Rs. {balance:,.0f}")
print("==================================")