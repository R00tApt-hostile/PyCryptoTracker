import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import threading
from datetime import datetime

class CryptoTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Tracker Pro")
        self.root.geometry("1000x700")
        
        self.api_url = "https://api.coingecko.com/api/v3"
        self.portfolio_file = "portfolio.json"
        self.update_interval = 60  # seconds
        self.currency = "USD"
        
        self.create_widgets()
        self.load_portfolio()
        self.update_data()
        self.schedule_updates()

    def create_widgets(self):
        # Notebook for multiple tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Price Tracker Tab
        self.tracker_tab = ttk.Frame(self.notebook)
        self.create_tracker_tab()
        
        # Portfolio Tab
        self.portfolio_tab = ttk.Frame(self.notebook)
        self.create_portfolio_tab()
        
        # Alerts Tab
        self.alerts_tab = ttk.Frame(self.notebook)
        self.create_alerts_tab()
        
        self.notebook.add(self.tracker_tab, text="Market Data")
        self.notebook.add(self.portfolio_tab, text="Portfolio")
        self.notebook.add(self.alerts_tab, text="Price Alerts")
        self.notebook.pack(expand=True, fill='both')

    def create_tracker_tab(self):
        # Market Data Table
        columns = ('rank', 'name', 'symbol', 'price', '24h_change', 'market_cap')
        self.tree = ttk.Treeview(self.tracker_tab, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col.replace('_', ' ').title())
            self.tree.column(col, width=120)
        
        self.tree.pack(expand=True, fill='both')
        
        # Currency selector
        self.currency_var = tk.StringVar(value=self.currency)
        self.currency_menu = ttk.Combobox(self.tracker_tab, textvariable=self.currency_var,
                                         values=['USD', 'EUR', 'GBP', 'BTC', 'ETH'])
        self.currency_menu.pack(side=tk.LEFT, padx=10)
        ttk.Button(self.tracker_tab, text="Refresh", command=self.update_data).pack(side=tk.RIGHT, padx=10)

    def create_portfolio_tab(self):
        # Portfolio List
        self.portfolio_tree = ttk.Treeview(self.portfolio_tab, 
                                          columns=('coin', 'amount', 'value', 'profit'), 
                                          show='headings')
        for col in ('coin', 'amount', 'value', 'profit'):
            self.portfolio_tree.heading(col, text=col.title())
        self.portfolio_tree.pack(expand=True, fill='both', side=tk.TOP)
        
        # Add/Remove controls
        control_frame = ttk.Frame(self.portfolio_tab)
        self.coin_var = tk.StringVar()
        ttk.Combobox(control_frame, textvariable=self.coin_var).pack(side=tk.LEFT)
        ttk.Entry(control_frame).pack(side=tk.LEFT)  # Amount entry
        ttk.Button(control_frame, text="Add", command=self.add_to_portfolio).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Remove", command=self.remove_from_portfolio).pack(side=tk.LEFT)
        control_frame.pack(side=tk.BOTTOM, pady=10)

    def create_alerts_tab(self):
        # Alert configuration
        self.alerts_list = tk.Listbox(self.alerts_tab)
        self.alerts_list.pack(expand=True, fill='both', side=tk.LEFT)
        
        alert_frame = ttk.Frame(self.alerts_tab)
        ttk.Combobox(alert_frame).pack()
        ttk.Entry(alert_frame).pack()  # Target price
        ttk.Button(alert_frame, text="Set Alert").pack()
        alert_frame.pack(side=tk.RIGHT)

    def schedule_updates(self):
        self.update_data()
        self.root.after(self.update_interval * 1000, self.schedule_updates)

    def update_data(self):
        threading.Thread(target=self._fetch_market_data).start()

    def _fetch_market_data(self):
        try:
            url = f"{self.api_url}/coins/markets"
            params = {
                'vs_currency': self.currency.lower(),
                'order': 'market_cap_desc',
                'per_page': 100
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            self.tree.delete(*self.tree.get_children())
            for coin in data:
                self.tree.insert('', 'end', values=(
                    coin['market_cap_rank'],
                    coin['name'],
                    coin['symbol'].upper(),
                    f"{coin['current_price']:,.2f}",
                    f"{coin['price_change_percentage_24h']:.2f}%",
                    f"{coin['market_cap']:,.0f}"
                ))
            
            self.update_portfolio_values()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

    def load_portfolio(self):
        try:
            with open(self.portfolio_file, 'r') as f:
                self.portfolio = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.portfolio = {}

    def save_portfolio(self):
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f)

    def add_to_portfolio(self):
        # Implementation for adding coins to portfolio
        pass

    def remove_from_portfolio(self):
        # Implementation for removing coins from portfolio
        pass

    def update_portfolio_values(self):
        # Implementation for updating portfolio values
        pass

    def check_price_alerts(self):
        # Implementation for price alerts
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoTracker(root)
    root.mainloop()
