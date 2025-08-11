import requests
from flask import Flask, render_template, request, redirect, url_for

import locale

# Set the locale to the user's default (you can also specify a particular locale)
locale.setlocale(locale.LC_ALL, '')

# Format a number with commas for thousands


def format_number_with_commas_and_decimals(number):
    formatted = locale.format_string("%.2f", number, grouping=True)
    return formatted


app = Flask(__name__)

api_key = "null"

# Portfolio data structure (a dictionary with stock symbols as keys and number of shares as values)
portfolio = {}


def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def add_stock_to_portfolio():
    symbol = request.form.get("symbol").upper()
    # Fetch the latest stock data
    data = fetch_stock_data(symbol)

    if is_valid_stock_data(data):
        latest_time = max(data["Time Series (5min)"].keys())
        latest_price = float(data["Time Series (5min)"]
                             [latest_time]["4. close"])

        if symbol not in portfolio:
            portfolio[symbol] = 0
        num_shares = int(request.form.get("num_shares"))

        portfolio[symbol] += num_shares
        result = f"Added {num_shares} shares of {symbol} at ${latest_price} per share to your portfolio."
    else:
        result = f"{symbol} is not a valid stock symbol or there was an issue fetching its data."

    return result  # Return the result as a string


def is_valid_stock_data(data):
    # Check if the data returned from the API response is valid
    if "Time Series (5min)" in data:
        return True
    return False


def remove_stock_from_portfolio(symbol):
    symbol = symbol.upper()
    if symbol in portfolio:
        num_shares = portfolio.pop(symbol)
        return f"Removed {num_shares} shares of {symbol} from your portfolio."
    else:
        return f"{symbol} is not in your portfolio."


def display_portfolio_summary():
    total_value = 0
    portfolio_summary = []

    for symbol, num_shares in portfolio.items():
        data = fetch_stock_data(symbol)

        if data is not None:
            latest_time = max(data["Time Series (5min)"].keys())
            latest_price = float(
                data["Time Series (5min)"][latest_time]["4. close"])
            stock_value = num_shares * latest_price
            total_value += stock_value
            portfolio_summary.append(
                (symbol, format_number_with_commas_and_decimals(num_shares), format_number_with_commas_and_decimals(
                    latest_price), format_number_with_commas_and_decimals(stock_value))
            )
        else:
            # If data cannot be retrieved, mark the stock with a placeholder value
            portfolio_summary.append(
                (symbol, format_number_with_commas_and_decimals(
                    num_shares), "N/A", "N/A")
            )

    return portfolio_summary, format_number_with_commas_and_decimals(total_value)


@ app.route('/')
def home():
    return render_template('index.html')


@ app.route('/portfolio_')
def portfolio_():  # You had an extra underscore here
    portfolio_summary, total_value = display_portfolio_summary()
    return render_template('portfolio_.html', portfolio=portfolio_summary, total_value=total_value)


@ app.route('/add_stock', methods=['POST'])
def add_stock():
    result = add_stock_to_portfolio()
    if "Added" in result:
        return redirect(url_for('portfolio_'))
    else:
        return result


@ app.route('/remove_stock', methods=['POST'])
def remove_stock():
    symbol = request.form.get("symbol").upper()
    result = remove_stock_from_portfolio(symbol)
    return result


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')

