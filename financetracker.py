import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def income():
    account_name = account_name_entry.get()
    amount = amount_entry.get()
    reason = reason_entry.get()
    try:
        amount = float(amount)
        accounts.append({'Account': account_name, 'Amount': amount, 'Reason': reason, 'Type': 'Income'})
        update_summary()
        update_charts()
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
        update_charts()
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
        update_charts()
        messagebox.showinfo("Success", "Transaction completed successfully.")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

def update_summary():
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, "Summary:\n", 'header')
    
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
        summary_text.insert(tk.END, f"{account}: {info['Amount']}\n", 'account')
        summary_text.insert(tk.END, "Reasons:\n", 'subheader')
        for reason in info['Reasons']:
            tag = 'income' if reason['Type'] == 'Income' else 'expense'
            summary_text.insert(tk.END, f"- {reason['Type']}: {reason['Amount']} - {reason['Reason']}\n", tag)
        summary_text.insert(tk.END, "Transactions:\n", 'subheader')
        for transaction in info['Transactions']:
            summary_text.insert(tk.END, f"- Transaction: {transaction['Amount']} - From: {transaction['From']} To: {transaction['To']}\n", 'transaction')

def show_net_worth_by_account():
    for widget in net_worth_canvas_frame.winfo_children():
        widget.destroy()
    
    account_summary = {}
    for entry in accounts:
        account = entry['Account']
        if account not in account_summary:
            account_summary[account] = 0
        account_summary[account] += entry['Amount']

    accounts_list = list(account_summary.keys())
    values = list(account_summary.values())

    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(values, labels=accounts_list, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    ax.set_title('Net Worth by Account')

    canvas = FigureCanvasTkAgg(fig, master=net_worth_canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def show_expenses_by_reason():
    for widget in expenses_canvas_frame.winfo_children():
        widget.destroy()
    
    reason_summary = {}
    for entry in accounts:
        if entry['Type'] == 'Expense':
            reason = entry['Reason']
            if reason not in reason_summary:
                reason_summary[reason] = 0
            reason_summary[reason] += -entry['Amount']

    reasons_list = list(reason_summary.keys())
    values = list(reason_summary.values())

    fig = Figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(values, labels=reasons_list, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    ax.set_title('Total Expenses by Reason')

    canvas = FigureCanvasTkAgg(fig, master=expenses_canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def update_charts():
    show_net_worth_by_account()
    show_expenses_by_reason()

accounts = []

root = tk.Tk()
root.title("SpendWise")

# Set window to fullscreen
root.state('zoomed')

# Set color scheme
bg_color = "#0f2027"  # Background color
fg_color = "#ffffff"  # White
text_color = "#000000"  # Black
highlight_color = "#4682b4"  # Steel blue
income_color = "#00ff00"  # Green for income
expense_color = "#ff0000"  # Red for expense

root.configure(bg=bg_color)

# Define styles
style = ttk.Style()
style.configure("TLabel", font=("Bahnschrift", 12), background=bg_color, foreground=fg_color)
style.configure("TButton", font=("Bahnschrift", 12), background=highlight_color, foreground=text_color, borderwidth=0, focusthickness=0)
style.configure("TEntry", font=("Bahnschrift", 12), foreground=text_color, fieldbackground=fg_color, borderwidth=0, focusthickness=0)
style.configure("TFrame", background=bg_color)
style.configure("TLabelframe", font=("Bahnschrift", 14, 'bold'), background=bg_color, foreground=fg_color)
style.configure("TLabelframe.Label", font=("Bahnschrift", 14, 'bold'), background=bg_color, foreground=fg_color)
style.map("TButton", background=[("active", highlight_color)], foreground=[("active", fg_color)])

# Create a main frame to center the content
main_frame = ttk.Frame(root)
main_frame.pack(expand=True, fill='both')

# Configure grid weights for main_frame
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.rowconfigure(0, weight=0)
main_frame.rowconfigure(1, weight=1)

# Title Label
title_label = ttk.Label(main_frame, text="SpendWise", font=("Bahnschrift", 24, 'bold'), background=bg_color, foreground=highlight_color)
title_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# Net Worth Chart Frame
net_worth_chart_frame = ttk.Frame(main_frame, padding=10)
net_worth_chart_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

net_worth_canvas_frame = ttk.Frame(net_worth_chart_frame)
net_worth_canvas_frame.pack(fill=tk.BOTH, expand=True)

# Middle Column for Income/Expense, Transaction, Summary
middle_frame = ttk.Frame(main_frame, padding=10)
middle_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Configure grid weights for middle_frame
middle_frame.rowconfigure(0, weight=1)
middle_frame.rowconfigure(1, weight=1)
middle_frame.rowconfigure(2, weight=1)

# Income/Expense Section
income_expense_frame = ttk.LabelFrame(middle_frame, text="Income/Expense", padding=10)
income_expense_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

account_name_label = ttk.Label(income_expense_frame, text="Account Name:")
account_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
account_name_entry = ttk.Entry(income_expense_frame, width=30)
account_name_entry.grid(row=0, column=1, padx=5, pady=5)

amount_label = ttk.Label(income_expense_frame, text="Amount:")
amount_label.grid(row=1, column=0, padx=5,pady=5, sticky="e")
amount_entry = ttk.Entry(income_expense_frame, width=30)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

reason_label = ttk.Label(income_expense_frame, text="Reason:")
reason_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
reason_entry = ttk.Entry(income_expense_frame, width=30)
reason_entry.grid(row=2, column=1, padx=5, pady=5)

income_button = ttk.Button(income_expense_frame, text="Add Income", command=income)
income_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

expense_button = ttk.Button(income_expense_frame, text="Add Expense", command=expense)
expense_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Transaction Section
transaction_frame = ttk.LabelFrame(middle_frame, text="Transaction", padding=10)
transaction_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

from_account_label = ttk.Label(transaction_frame, text="From Account:")
from_account_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
from_account_entry = ttk.Entry(transaction_frame, width=30)
from_account_entry.grid(row=0, column=1, padx=5, pady=5)

to_account_label = ttk.Label(transaction_frame, text="To Account:")
to_account_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
to_account_entry = ttk.Entry(transaction_frame, width=30)
to_account_entry.grid(row=1, column=1, padx=5, pady=5)

transaction_amount_label = ttk.Label(transaction_frame, text="Transaction Amount:")
transaction_amount_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
transaction_amount_entry = ttk.Entry(transaction_frame, width=30)
transaction_amount_entry.grid(row=2, column=1, padx=5, pady=5)

transaction_button = ttk.Button(transaction_frame, text="Make Transaction", command=transaction)
transaction_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Summary Section
summary_frame = ttk.LabelFrame(middle_frame, text="Summary", padding=10)
summary_frame.grid(row=2, column=0, sticky="nsew")

net_worth_label = ttk.Label(summary_frame, text="Net Worth: 0")
net_worth_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

summary_text = tk.Text(summary_frame, height=10, width=60, font=('Bahnschrift', 10), bg=fg_color, fg=text_color)
summary_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

summary_text.tag_configure('header', font=('Bahnschrift', 12, 'bold'), foreground=highlight_color)
summary_text.tag_configure('account', font=('Bahnschrift', 11, 'bold'), foreground=highlight_color)
summary_text.tag_configure('subheader', font=('Bahnschrift', 10, 'bold'), foreground=highlight_color)
summary_text.tag_configure('income', foreground=income_color)
summary_text.tag_configure('expense', foreground=expense_color)
summary_text.tag_configure('transaction', foreground=text_color)

# Expense Chart Frame
expense_chart_frame = ttk.Frame(main_frame, padding=10)
expense_chart_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

expenses_canvas_frame = ttk.Frame(expense_chart_frame)
expenses_canvas_frame.pack(fill=tk.BOTH, expand=True)

update_summary()
update_charts()

root.mainloop()

#next update should be on changing the entire file to HTML, CSS and JS with some modifications