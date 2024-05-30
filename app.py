from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
from account import Account

app = Flask(__name__)
account = Account()

def get_stock_data(symbol, period='1mo', interval='1d'):
    ticker = yf.Ticker(symbol)
    try:
        df = ticker.history(period=period, interval=interval)
        if not df.empty:
            return df
        else:
            raise ValueError("No data found for the symbol")
    except Exception as e:
        print(f"Error retrieving data for {symbol}: {e}")
        return pd.DataFrame()

@app.route('/')
def home():
    initial_symbol = 'AAPL'
    initial_data = get_stock_data(initial_symbol)
    return render_template('index.html', balance=account.balance, portfolio=account.portfolio, initial_data=initial_data.to_json(orient='split'), initial_symbol=initial_symbol)

@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.get_json()
    symbol = data['symbol']
    stock_data = get_stock_data(symbol)
    if not stock_data.empty:
        return stock_data.to_json(orient='split')
    else:
        return jsonify(success=False, message="No data found for the symbol"), 404

@app.route('/buy', methods=['POST'])
def buy():
    data = request.get_json()
    print("Received buy request data:", data)
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    if not symbol or not quantity:
        return jsonify(success=False, message="Symbol and quantity are required"), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify(success=False, message="Quantity must be an integer"), 400

    price = account.get_stock_price(symbol)
    if price is not None:
        if account.buy_stock(symbol, quantity, price):
            return jsonify(success=True, balance=account.balance, portfolio=account.portfolio)
        else:
            return jsonify(success=False, message="Insufficient funds"), 400
    else:
        return jsonify(success=False, message="Error retrieving stock price"), 400


@app.route('/sell', methods=['POST'])
def sell():
    data = request.get_json()
    symbol = data['symbol']
    quantity = int(data['quantity'])
    price = account.get_stock_price(symbol)
    if price is not None:
        if account.sell_stock(symbol, quantity, price):
            return jsonify(success=True, balance=account.balance, portfolio=account.portfolio)
        else:
            return jsonify(success=False, message="Insufficient shares"), 400
    else:
        return jsonify(success=False, message="Error retrieving stock price"), 400

@app.route('/portfolio')
def portfolio():
    return jsonify(balance=account.balance, portfolio=account.portfolio)

if __name__ == '__main__':
    app.run(debug=True)
