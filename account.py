import pandas as pd
import yfinance as yf

class Account:
    def __init__(self, initial_balance=100000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.portfolio = {}
        self.transaction_history = pd.DataFrame(columns=['Date', 'Type', 'Symbol', 'Quantity', 'Price', 'Total'])

    def reset_account(self):
        self.balance = self.initial_balance
        self.portfolio = {}
        self.transaction_history = pd.DataFrame(columns=['Date', 'Type', 'Symbol', 'Quantity', 'Price', 'Total'])

    def buy_stock(self, symbol, quantity, price):
        cost = quantity * price
        if cost <= self.balance:
            self.balance -= cost
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
            self.transaction_history = self.transaction_history.append({
                'Date': pd.Timestamp.now(),
                'Type': 'BUY',
                'Symbol': symbol,
                'Quantity': quantity,
                'Price': price,
                'Total': cost
            }, ignore_index=True)
            return True
        return False

    def sell_stock(self, symbol, quantity, price):
        if symbol in self.portfolio and self.portfolio[symbol] >= quantity:
            revenue = quantity * price
            self.balance += revenue
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
            self.transaction_history = self.transaction_history.append({
                'Date': pd.Timestamp.now(),
                'Type': 'SELL',
                'Symbol': symbol,
                'Quantity': quantity,
                'Price': price,
                'Total': revenue
            }, ignore_index=True)
            return True
        return False

    def get_portfolio_value(self):
        return self.balance + sum([self.get_stock_price(symbol) * qty for symbol, qty in self.portfolio.items()])

    def get_stock_price(self, symbol):
        ticker = yf.Ticker(symbol)
        try:
            data = ticker.history(period='1d')
            if not data.empty:
                return data['Close'].iloc[-1]
            else:
                raise ValueError("No data found for the symbol")
        except Exception as e:
            print(f"Error retrieving data for {symbol}: {e}")
            return None
