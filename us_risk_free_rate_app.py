import yfinance as yf
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class RiskFreeRateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Risk-Free Rate Calculator")

        # Create labels and entry widgets
        ttk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_date_entry = ttk.Entry(root, width=15)
        self.start_date_entry.insert(0, "YYYY-MM-DD")
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.end_date_entry = ttk.Entry(root, width=15)
        self.end_date_entry.insert(0, "YYYY-MM-DD")
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create the "Get Risk-Free Rate" button
        ttk.Button(root, text="Get Risk-Free Rate", command=self.get_risk_free_rate).grid(row=2, column=0, columnspan=2, pady=10)

        # Create a label to display the result
        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def get_user_input(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            # Parse the date inputs
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            self.result_label.config(text="Error: Please enter valid dates in the format YYYY-MM-DD.")
            return None, None

        return start_date, end_date

    def get_risk_free_rate(self):
        start_date, end_date = self.get_user_input()

        if start_date is None or end_date is None:
            return

        # USA 10-year Treasury yield ticker
        bond_ticker = "^IRX"

        # Fetch historical bond prices
        bond_data = yf.download(bond_ticker, start=start_date, end=end_date)['Adj Close']

        if bond_data.empty:
            self.result_label.config(text=f"Error: Unable to fetch data for the USA.")
            return

        # Calculate the average yield as the risk-free rate
        risk_free_rate = bond_data.mean()

        # Display result
        result_text = f"Risk-Free Rate for the USA from {start_date} to {end_date}: {risk_free_rate:.4f}%"
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = RiskFreeRateApp(root)
    root.mainloop()
