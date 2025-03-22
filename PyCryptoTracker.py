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
        self.alerts_file = "alerts.json"
        self.update_interval = 60  # seconds
        self.currency = "USD"
        
        self.portfolio = {}
        self.alerts = []
        
        self.create_widgets()
        self.load_data()
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
        self.coin_menu = ttk.Combobox(control_frame, textvariable=self.coin_var)
        self.coin_menu.pack(side=tk.LEFT, padx=5)
        
        self.amount_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.amount_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Add", command=self.add_to_portfolio).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Remove", command=self.remove_from_portfolio).pack(side=tk.LEFT, padx=5)
        control_frame.pack(side=tk.BOTTOM, pady=10)

    def create_alerts_tab(self):
        # Alert List
        self.alerts_list = tk.Listbox(self.alerts_tab)
        self.alerts_list.pack(expand=True, fill='both', side=tk.LEFT)
        
        # Alert Configuration
        alert_frame = ttk.Frame(self.alerts_tab)
        
        self.alert_coin_var = tk.StringVar()
        self.alert_coin_menu = ttk.Combobox(alert_frame, textvariable=self.alert_coin_var)
        self.alert_coin_menu.pack(pady=5)
        
        self.alert_price_var = tk.StringVar()
        ttk.Entry(alert_frame, textvariable=self.alert_price_var, width=10).pack(pady=5)
        
        ttk.Button(alert_frame, text="Set Alert", command=self.set_alert).pack(pady=5)
        ttk.Button(alert_frame, text="Remove Alert", command=self.remove_alert).pack(pady=5)
        alert_frame.pack(side=tk.RIGHT, padx=10)

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
            
            # Update market data table
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
            
            # Update coin dropdowns
            coin_names = [coin['id'] for coin in data]
            self.coin_menu['values'] = coin_names
            self.alert_coin_menu['values'] = coin_names
            
            # Update portfolio and alerts
            self.update_portfolio_values()
            self.check_price_alerts()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

    def load_data(self):
        try:
            with open(self.portfolio_file, 'r') as f:
                self.portfolio = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.portfolio = {}
        
        try:
            with open(self.alerts_file, 'r') as f:
                self.alerts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.alerts = []

    def save_data(self):
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f)
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f)

    def add_to_portfolio(self):
        coin = self.coin_var.get()
        amount = self.amount_var.get()
        
        if not coin or not amount:
            messagebox.showwarning("Input Error", "Please select a coin and enter an amount.")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a positive number.")
            return
        
        self.portfolio[coin] = self.portfolio.get(coin, 0) + amount
        self.save_data()
        self.update_portfolio_values()
        messagebox.showinfo("Success", f"Added {amount} of {coin} to your portfolio.")

    def remove_from_portfolio(self):
        coin = self.coin_var.get()
        if not coin or coin not in self.portfolio:
            messagebox.showwarning("Input Error", "Coin not found in portfolio.")
            return
        
        self.portfolio.pop(coin)
        self.save_data()
        self.update_portfolio_values()
        messagebox.showinfo("Success", f"Removed {coin} from your portfolio.")

    def update_portfolio_values(self):
        self.portfolio_tree.delete(*self.portfolio_tree.get_children())
        total_value = 0
        
        for coin, amount in self.portfolio.items():
            price = self.get_coin_price(coin)
            if price:
                value = amount * price
                total_value += value
                self.portfolio_tree.insert('', 'end', values=(
                    coin, amount, f"${value:,.2f}", "N/A"
                ))
        
        # Update total portfolio value
        self.portfolio_tree.insert('', 'end', values=(
            "Total", "", f"${total_value:,.2f}", ""
        ))

    def get_coin_price(self, coin_id):
        url = f"{self.api_url}/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': self.currency.lower()
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get(coin_id, {}).get(self.currency.lower(), 0)
        return 0

    def set_alert(self):
        coin = self.alert_coin_var.get()
        price = self.alert_price_var.get()
        
        if not coin or not price:
            messagebox.showwarning("Input Error", "Please select a coin and enter a target price.")
            return
        
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Target price must be a positive number.")
            return
        
        self.alerts.append({'coin': coin, 'target_price': price})
        self.save_data()
        self.update_alerts_list()
        messagebox.showinfo("Success", f"Alert set for {coin} at ${price:,.2f}.")

    def remove_alert(self):
        selected = self.alerts_list.curselection()
        if not selected:
            messagebox.showwarning("Input Error", "Please select an alert to remove.")
            return
        
        self.alerts.pop(selected[0])
        self.save_data()
        self.update_alerts_list()
        messagebox.showinfo("Success", "Alert removed.")

    def update_alerts_list(self):
        self.alerts_list.delete(0, tk.END)
        for alert in self.alerts:
            self.alerts_list.insert(tk.END, f"{alert['coin']} - ${alert['target_price']:,.2f}")

    def check_price_alerts(self):
        for alert in self.alerts:
            coin = alert['coin']
            target_price = alert['target_price']
            current_price = self.get_coin_price(coin)
            
            if current_price and current_price >= target_price:
                messagebox.showinfo("Price Alert", f"{coin} has reached your target price of ${target_price:,.2f}!")
                self.alerts.remove(alert)
                self.save_data()
                self.update_alerts_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoTracker(root)
    root.mainloop()
