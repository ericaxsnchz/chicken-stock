import pandas as pd
import yfinance as yf
from datetime import datetime, timezone

class Account:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.portfolio = {}
        self.transaction_history = pd.DataFrame(columns=['Date', 'Symbol', 'Quantity', 'Price', 'Total'])
        self.daily_portfolio_value = pd.DataFrame(columns=['Date', 'Value'])

    def get_stock_data(self, symbol):
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
                'Date': datetime.now(timezone.utc),
                'Symbol': symbol,
                'Quantity': quantity,
                'Price': price,
                'Total': total_cost
            }])
            
            if not new_transaction.empty:
                self.transaction_history = pd.concat([self.transaction_history, new_transaction], ignore_index=True)
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
                'Date': datetime.now(timezone.utc),
                'Symbol': symbol,
                'Quantity': -quantity,
                'Price': price,
                'Total': total_revenue
            }])
            
            if not new_transaction.empty:
                self.transaction_history = pd.concat([self.transaction_history, new_transaction], ignore_index=True)
            self.update_daily_portfolio_value()
            return True
        else:
            return False

    def update_daily_portfolio_value(self):
        total_stock_values = sum([self.get_stock_price(symbol) * qty for symbol, qty in self.portfolio.items()])

        total_transactions = self.transaction_history['Total'].sum()

        total_value = round(self.balance + total_stock_values - total_transactions, 2)

        today_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        new_value = pd.DataFrame({'Date': [today_date], 'Value': [total_value]})
        
        print("New Daily Portfolio Value:")
        print(new_value)
        
        if self.daily_portfolio_value.empty:
            self.daily_portfolio_value = new_value
        else:
            self.daily_portfolio_value = pd.concat([self.daily_portfolio_value, new_value], ignore_index=True)
        
        print("Updated Daily Portfolio Values:")
        print(self.daily_portfolio_value)

    def get_daily_portfolio_value(self):
        data = self.daily_portfolio_value.copy()
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date') 
        return {
            'index': data.index.strftime('%Y-%m-%d').tolist(),
            'data': data['Value'].tolist()
        }

    def get_portfolio_value(self):
        balance_value = self.balance
        stock_values = sum([self.get_stock_price(symbol) * qty for symbol, qty in self.portfolio.items()])
        total_value = round(balance_value + stock_values, 2)
        print(f"Current Portfolio Value: {total_value} (Balance: {self.balance}, Stocks: {stock_values})")
        return total_value

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
            return 0
