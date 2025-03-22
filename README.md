# Crypto Tracker Pro 🚀

**Crypto Tracker Pro** is a comprehensive Python-based cryptocurrency tracking toolkit with a user-friendly GUI. It allows you to monitor real-time cryptocurrency prices, manage your portfolio, and set price alerts—all in one place. Built with `Tkinter` for the interface and powered by the **CoinGecko API**, this application is perfect for both casual users and crypto enthusiasts.

---

## Features ✨

- **Real-Time Market Data**:
  - Track the top 100 cryptocurrencies by market cap.
  - View prices, 24-hour changes, and market caps in multiple currencies (USD, EUR, GBP, BTC, ETH).
  - Auto-refreshes every 60 seconds.

- **Portfolio Management**:
  - Add and remove cryptocurrencies from your portfolio.
  - Track the total value of your holdings in real-time.
  - Save your portfolio locally for persistence across sessions.

- **Price Alerts**:
  - Set target prices for specific cryptocurrencies.
  - Get notified when your target prices are reached.
  - Manage and remove alerts easily.

- **User-Friendly Interface**:
  - Intuitive tabbed layout for seamless navigation.
  - Responsive design with real-time updates.

- **Data Persistence**:
  - Portfolio and alerts are saved to local JSON files (`portfolio.json` and `alerts.json`).
  - Data persists between application restarts.

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/crypto-tracker-pro.git
   cd crypto-tracker-pro
   ```

2. Install the required dependencies:
   ```bash
   pip install requests
   ```

3. Run the application:
   ```bash
   python crypto_tracker.py
   ```

---

## Usage 🖥️

1. **Market Data Tab**:
   - View real-time cryptocurrency prices.
   - Change the currency using the dropdown menu.

2. **Portfolio Tab**:
   - Add cryptocurrencies to your portfolio by selecting a coin and entering the amount.
   - Remove coins from your portfolio as needed.
   - Track the total value of your holdings.

3. **Alerts Tab**:
   - Set price alerts by selecting a coin and entering a target price.
   - Remove alerts when they are no longer needed.
   - Receive notifications when your target prices are reached.

---

## File Structure 📂

```
crypto-tracker-pro/
├── crypto_tracker.py       # Main application script
├── portfolio.json          # Portfolio data (auto-generated)
├── alerts.json             # Alerts data (auto-generated)
├── README.md               # Project documentation
└── screenshots/            # Screenshots for the README
```

---

## Contributing 🤝

Contributions are welcome! If you'd like to improve Crypto Tracker Pro, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## License 📜

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙏

- Powered by the [CoinGecko API](https://www.coingecko.com/).
- Built with Python and `Tkinter`.

---
