import pandas as pd
import yfinance as yf

class Account:
    def __init__(self):
        self.balance = 10000
        self.portfolio = {}
        self.transaction_history = pd.DataFrame(columns=['Symbol', 'Action', 'Quantity', 'Price', 'Total'])

    def get_stock_price(self, symbol):
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if not data.empty:
            return data['Close'].iloc[-1]
        else:
            print(f"Error retrieving data for {symbol}")
            return None

    def buy_stock(self, symbol, quantity, price):
        if self.balance >= quantity * price:
            total_cost = quantity * price
            self.balance -= total_cost
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
            new_transaction = pd.DataFrame({'Symbol': [symbol], 'Action': ['Buy'], 'Quantity': [quantity], 'Price': [price], 'Total': [total_cost]})
            if self.transaction_history.empty:
                self.transaction_history = new_transaction
            else:
                self.transaction_history = pd.concat([self.transaction_history, new_transaction], ignore_index=True)
            return True
        else:
            return False

    def sell_stock(self, symbol, quantity, price):
        if symbol in self.portfolio and self.portfolio[symbol] >= quantity:
            total_revenue = price * quantity
            self.balance += total_revenue
            self.portfolio[symbol] -= quantity

            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]

            new_transaction = pd.DataFrame([{
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'total': total_revenue,
                'type': 'sell'
            }])

            self.transaction_history = pd.concat([self.transaction_history, new_transaction], ignore_index=True)
            return True
        else:
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
