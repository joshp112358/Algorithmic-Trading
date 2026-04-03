import pandas as pd
def signal_generation(stock,data_all,strategy):
    """
    Generate trading signals for a given stock and strategy.
    
    Parameters:
        stock (str): The stock ticker (e.g., "AAPL").
        data_all (pd.DataFrame): A dictionary-like DataFrame with keys "Close" and "Volume".
                                 Each of these should be a DataFrame with stock tickers as columns.
        strategy (str): The trading strategy to apply. Options are:
                        "momentum", "mean_reversion", "breakout", "rsi", "macd", "vwap".
    
    Returns:
        tuple: (long_signal, short_signal, additional_indicators)
               - long_signal (pd.Series): Boolean series indicating long trade signals.
               - short_signal (pd.Series): Boolean series indicating short trade signals.
               - additional_indicators (list): List of Series with key indicators used in the strategy.
    """
    data=data_all["Close"]
    if strategy == "momentum":
        short_window = 50
        long_window = 100
        short_ma = data[stock].rolling(window=short_window).mean()
        long_ma = data[stock].rolling(window=long_window).mean()
        long_signal = short_ma > long_ma 
        short_signal = short_ma < long_ma 
        return long_signal, short_signal,[short_ma,long_ma]
    elif strategy == "mean_reversion":
        long_window = 100
        rolling_mean = data[stock].rolling(window=long_window).mean()
        rolling_std = data[stock].rolling(window=long_window).std()
        upper_band = rolling_mean + (2 * rolling_std)
        lower_band = rolling_mean - (2 * rolling_std)
        long_signal = data[stock] < lower_band  # Buy when price is low
        short_signal = data[stock] > upper_band  # Sell when price is high
        return long_signal, short_signal,[upper_band,lower_band,rolling_mean]
    elif strategy == "breakout":
        high_20 = data[stock].rolling(window=20).max()
        low_20 = data[stock].rolling(window=20).min()
        long_signal = data[stock] >= high_20
        short_signal = data[stock] <= low_20
        return long_signal, short_signal,[high_20,low_20]
    elif strategy == "rsi":
        delta = data[stock].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        long_signal = rsi < 30
        short_signal = rsi > 70
        return long_signal, short_signal,[rsi]
    elif strategy == "macd":
        short_ema = data[stock].ewm(span=12, adjust=False).mean()
        long_ema = data[stock].ewm(span=26, adjust=False).mean()
        macd = short_ema - long_ema
        signal_line = macd.ewm(span=9, adjust=False).mean()
        long_signal = macd > signal_line
        short_signal = macd < signal_line
        return long_signal, short_signal,[short_ema,long_ema,signal_line]
    elif strategy == "vwap":
        vwap = (data_all["Close"][stock] * data_all['Volume'][stock]).rolling(window=50).sum() / data_all['Volume'][stock].rolling(window=50).sum()
        long_signal = data[stock] > vwap
        short_signal = data[stock] < vwap
        return long_signal, short_signal,[vwap]
    else:
        raise ValueError("Unsupported strategy")