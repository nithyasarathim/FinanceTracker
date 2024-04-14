import tkinter as tk
from tkinter import messagebox

def income():
    account_name = account_name_entry.get()
    amount = amount_entry.get()
    reason = reason_entry.get()
    try:
        amount = float(amount)
        accounts.append({'Account': account_name, 'Amount': amount, 'Reason': reason, 'Type': 'Income'})
        update_summary()
        messagebox.showinfo("Success", "Income added successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

def expense():
    account_name = account_name_entry.get()
    amount = amount_entry.get()
    reason = reason_entry.get()
    try:
        amount = float(amount)
        accounts.append({'Account': account_name, 'Amount': -amount, 'Reason': reason, 'Type': 'Expense'})
        update_summary()
        messagebox.showinfo("Success", "Expense added successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

def transaction():
    from_account = from_account_entry.get()
    to_account = to_account_entry.get()
    amount = transaction_amount_entry.get()
    try:
        amount = float(amount)
        accounts.append({'Account': from_account, 'Amount': -amount, 'Type': 'Transaction'})
        accounts.append({'Account': to_account, 'Amount': amount, 'Type': 'Transaction'})
        update_summary()
        messagebox.showinfo("Success", "Transaction completed successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

def update_summary():
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, "Summary:\n")
    
    summary = {}
    net_worth = 0
    for entry in accounts:
        account = entry['Account']
        if account not in summary:
            summary[account] = {'Amount': 0, 'Reasons': [], 'Transactions': []}
        summary[account]['Amount'] += entry['Amount']
        net_worth += entry['Amount']
        if entry['Type'] in ['Income', 'Expense']:
            summary[account]['Reasons'].append({'Type': entry['Type'], 'Amount': entry['Amount'], 'Reason': entry.get('Reason', '')})
        elif entry['Type'] == 'Transaction':
            summary[account]['Transactions'].append({'From': account, 'To': next(acc['Account'] for acc in accounts if acc['Type'] == 'Transaction' and acc['Account'] != account), 'Amount': entry['Amount']})

    net_worth_label.config(text=f"Net Worth: {net_worth}")
    for account, info in summary.items():
        summary_text.insert(tk.END, f"{account}: {info['Amount']}\n")
        summary_text.insert(tk.END, "Reasons:\n")
        for reason in info['Reasons']:
            summary_text.insert(tk.END, f"- {reason['Type']}: {reason['Amount']} - {reason['Reason']}\n")
        summary_text.insert(tk.END, "Transactions:\n")
        for transaction in info['Transactions']:
            summary_text.insert(tk.END, f"- Transaction: {transaction['Amount']} - From: {transaction['From']} To: {transaction['To']}\n")

accounts = []

root = tk.Tk()
root.title("Finance Tracker")

# Create UI elements
account_name_label = tk.Label(root, text="Account Name:")
account_name_label.grid(row=0, column=0, padx=5, pady=5)
account_name_entry = tk.Entry(root)
account_name_entry.grid(row=0, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

reason_label = tk.Label(root, text="Reason:")
reason_label.grid(row=2, column=0, padx=5, pady=5)
reason_entry = tk.Entry(root)
reason_entry.grid(row=2, column=1, padx=5, pady=5)

income_button = tk.Button(root, text="Add Income", command=income)
income_button.grid(row=3, column=0, padx=5, pady=5)

expense_button = tk.Button(root, text="Add Expense", command=expense)
expense_button.grid(row=3, column=1, padx=5, pady=5)

from_account_label = tk.Label(root, text="From Account:")
from_account_label.grid(row=4, column=0, padx=5, pady=5)
from_account_entry = tk.Entry(root)
from_account_entry.grid(row=4, column=1, padx=5, pady=5)

to_account_label = tk.Label(root, text="To Account:")
to_account_label.grid(row=5, column=0, padx=5, pady=5)
to_account_entry = tk.Entry(root)
to_account_entry.grid(row=5, column=1, padx=5, pady=5)

transaction_amount_label = tk.Label(root, text="Transaction Amount:")
transaction_amount_label.grid(row=6, column=0, padx=5, pady=5)
transaction_amount_entry = tk.Entry(root)
transaction_amount_entry.grid(row=6, column=1, padx=5, pady=5)

transaction_button = tk.Button(root, text="Make Transaction", command=transaction)
transaction_button.grid(row=7, columnspan=2, padx=5, pady=5)

net_worth_label = tk.Label(root, text="Net Worth: 0")
net_worth_label.grid(row=8, columnspan=2, padx=5, pady=5)

summary_text = tk.Text(root, height=10, width=60, font=('Bahnschrift', 10))
summary_text.grid(row=9, columnspan=2, padx=5, pady=5)

update_summary()

root.mainloop()

