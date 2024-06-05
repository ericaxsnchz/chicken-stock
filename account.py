import yfinance as yf
from datetime import datetime, timezone

class Account:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.portfolio = {}
        self.transaction_history = []
        self.daily_portfolio_value = []

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

            new_transaction = {
                'Date': datetime.now(timezone.utc),
                'Symbol': symbol,
                'Quantity': quantity,
                'Price': price,
                'Total': total_cost
            }
            
            self.transaction_history.append(new_transaction)
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

            new_transaction = {
                'Date': datetime.now(timezone.utc),
                'Symbol': symbol,
                'Quantity': quantity,
                'Price': price,
                'Total': total_revenue
            }
            
            self.transaction_history.append(new_transaction)
            self.update_daily_portfolio_value()
            return True
        else:
            return False

    def update_daily_portfolio_value(self):
        total_stock_values = 0
        total_buying_costs = 0

        for symbol in self.portfolio.keys():
            symbol_transactions = [t for t in self.transaction_history if t['Symbol'] == symbol]

            total_quantity = sum(t['Quantity'] for t in symbol_transactions)
            total_cost = sum(t['Total'] for t in symbol_transactions)

            stock_value = total_quantity * self.get_stock_price(symbol)

            if total_cost > 0:
                total_buying_costs += total_cost

            total_stock_values += stock_value

        total_value = round(self.balance + total_stock_values - total_buying_costs, 2)

        today_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        new_value = {'Date': today_date, 'Value': total_value}

        self.daily_portfolio_value.append(new_value)

    def get_daily_portfolio_value(self):
        return {
            'index': [v['Date'] for v in self.daily_portfolio_value],
            'data': ['${:,.2f}'.format(v['Value']) for v in self.daily_portfolio_value]
        }

    def get_portfolio_value(self):
        balance_value = self.balance
        stock_values = sum([self.get_stock_price(symbol) * qty for symbol, qty in self.portfolio.items()])
        total_value = round(balance_value + stock_values, 2)
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
            return 0
