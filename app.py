from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
from account import Account

app = Flask(__name__)
account = Account()

def get_stock_price(symbol, period='1mo', interval='1d'):
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

def get_current_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    try:
        df = ticker.history(period='1d', interval='1d')
        if not df.empty:
            return df['Close'].iloc[-1]
        else:
            raise ValueError("No data found for the symbol")
    except Exception as e:
        print(f"Error retrieving current price for {symbol}: {e}")
        return None

@app.route('/')
def home():
    initial_symbol = 'AAPL'
    initial_data = get_stock_price(initial_symbol)
    return render_template('index.html', balance=account.balance, portfolio=account.portfolio, initial_data=initial_data.to_json(orient='split'), initial_symbol=initial_symbol)

@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.get_json()
    symbol = data.get('symbol')
    
    if symbol is None:
        return jsonify({"error": "No symbol provided"}), 400

    stock_data = get_stock_price(symbol)
    current_price = get_current_stock_price(symbol)
    if stock_data.empty or current_price is None:
        return jsonify({"error": "Unable to fetch data for the symbol"}), 500

    return jsonify({
        "index": stock_data.index.strftime('%Y-%m-%d').tolist(),
        "data": stock_data.values.tolist(),
        "current_price": current_price
    })

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    symbol = data['symbol']
    quantity = data['quantity']
    price = account.get_stock_price(symbol)
    total_cost = quantity * price
    success = account.buy_stock(symbol, quantity, price)
    if success:
        return jsonify(balance=account.balance, portfolio=account.portfolio, total_cost=total_cost)
    else:
        return jsonify(error="Insufficient funds"), 400

@app.route('/sell', methods=['POST'])
def sell():
    data = request.json
    symbol = data['symbol']
    quantity = data['quantity']
    price = account.get_stock_price(symbol)
    total_revenue = quantity * price
    success = account.sell_stock(symbol, quantity, price)
    if success:
        return jsonify(balance=account.balance, portfolio=account.portfolio, total_revenue=total_revenue)
    else:
        return jsonify(error="Not enough stock"), 400

def update_portfolio_chart():
    data = account.get_daily_portfolio_value()
    return jsonify(data)

@app.route('/portfolio')
def portfolio():
    return jsonify(balance=account.balance, portfolio=account.portfolio)

@app.route('/portfolio_value', methods=['GET'])
def portfolio_value():
    portfolio_data = account.get_daily_portfolio_value()
    return jsonify(portfolio_data=portfolio_data)

if __name__ == '__main__':
    app.run(debug=True)
