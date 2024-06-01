import pandas as pd
import yfinance as yf
from datetime import datetime

class Account:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.portfolio = {}
        self.transaction_history = pd.DataFrame(columns=['Date', 'Symbol', 'Quantity', 'Price', 'Total'])
        self.daily_portfolio_value = pd.DataFrame(columns=['Date', 'Value'])

    def get_stock_price(self, symbol):
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        return todays_data['Close'][0]

    def buy_stock(self, symbol, quantity, price):
        total_cost = quantity * price
        if total_cost <= self.balance:
            self.balance -= total_cost
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity

            new_transaction = pd.DataFrame([{
                'Date': datetime.now(),
                'Symbol': symbol,
                'Quantity': quantity,
                'Price': price,
                'Total': total_cost
            }])
            if not self.transaction_history.empty:
                self.transaction_history = pd.concat([self.transaction_history, new_transaction], ignore_index=True)
            else:
                self.transaction_history = new_transaction
            self.update_daily_portfolio_value()
            return True
        else:
            return False

    def sell_stock(self, symbol, quantity, price):
        if symbol in self.portfolio and self.portfolio[symbol] >= quantity:
            total_revenue = quantity * price
            self.balance += total_revenue
            self.portfolio[symbol] -= quantity
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]

            new_transaction = pd.DataFrame([{
                'Date': datetime.now(),
                'Symbol': symbol,
                'Quantity': -quantity,
                'Price': price,
                'Total': total_revenue
            }])
            if not self.transaction_history.empty:
                self.transaction_history = pd.concat([self.transaction_history, new_transaction], ignore_index=True)
            else:
                self.transaction_history = new_transaction
            self.update_daily_portfolio_value()
            return True
        else:
            return False

    def update_daily_portfolio_value(self):
        date = datetime.now().date()
        total_value = self.balance + sum(self.get_stock_price(symbol) * quantity for symbol, quantity in self.portfolio.items())
        new_value = pd.DataFrame({'Date': [date], 'Value': [total_value]})
        if self.daily_portfolio_value.empty:
            self.daily_portfolio_value = new_value
        else:
            self.daily_portfolio_value = pd.concat([self.daily_portfolio_value, new_value], ignore_index=True, sort=False)




    def get_daily_portfolio_value(self):
        return self.daily_portfolio_value.sort_values(by='Date')

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
