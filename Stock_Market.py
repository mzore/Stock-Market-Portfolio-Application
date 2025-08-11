"""
Author:  Matthew Zoretich
__updated__ = "2023-10-20"
-------------------------------------------------------
"""

import requests

api_key = "null"

# Portfolio data structure (a dictionary with stock symbols as keys and number of shares as values)
portfolio = {}


def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def add_stock_to_portfolio():
    symbol = input("Enter stock symbol: ").upper()

    # Fetch the latest stock data
    data = fetch_stock_data(symbol)

    if is_valid_stock_data(data):
        latest_time = max(data["Time Series (5min)"].keys())
        latest_price = float(data["Time Series (5min)"]
                             [latest_time]["4. close"])

        if symbol not in portfolio:
            portfolio[symbol] = 0
        num_shares = int(
            input(f"Enter the number of shares of {symbol} to add: "))

        portfolio[symbol] += num_shares
        print(
            f"Added {num_shares} shares of {symbol} at ${latest_price} per share to your portfolio.")
    else:
        print(
            f"{symbol} is not a valid stock symbol or there was an issue fetching its data.")


def is_valid_stock_data(data):
    # Check if the data returned from the API response is valid
    if "Time Series (5min)" in data:
        return True
    return False


def remove_stock_from_portfolio():
    symbol = input("Enter stock symbol to remove: ").upper()
    if symbol in portfolio:
        num_shares = portfolio.pop(symbol)
        print(f"Removed {num_shares} shares of {symbol} from your portfolio.")
    else:
        print(f"{symbol} is not in your portfolio.")


def analyze_portfolio():
    print("\nPortfolio Summary:")
    total_value = 0
    for symbol, num_shares in portfolio.items():
        data = fetch_stock_data(symbol)
        latest_time = max(data["Time Series (5min)"].keys())
        latest_price = float(data["Time Series (5min)"]
                             [latest_time]["4. close"])
        stock_value = num_shares * latest_price
        total_value += stock_value
        print(
            f"{symbol}: {num_shares} shares, Current Price: ${latest_price}, Value: ${stock_value:.2f}")
    print(f"Total Portfolio Value: ${total_value:.2f}")


def main():
    while True:
        print("\nStock Portfolio Manager")
        print("1. Add Stock to Portfolio")
        print("2. Remove Stock from Portfolio")
        print("3. Analyze Portfolio")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            add_stock_to_portfolio()
        elif choice == "2":
            remove_stock_from_portfolio()
        elif choice == "3":
            analyze_portfolio()
        elif choice == "4":
            print("Exiting the portfolio manager.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()

