import yfinance as yf

def get_stock_data(symbol, period='1mo', interval='1d'):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    return df
