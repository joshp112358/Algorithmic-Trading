import pandas as pd
import numpy as np
from signal_generator import signal_generation
from trade_simulator import Trade_Simulator
from sklearn.preprocessing import StandardScaler

def get_lookback_days(strategy):
    """Returns extra lookback days required for each strategy"""
    if strategy in ["momentum", "mean_reversion"]:
        return 100  # Needs long-term MA
    elif strategy in ["macd","vwap"]:
        return 60  # Needs medium-term indicators
    elif strategy in ["breakout", "rsi"]:
        return 30  # Needs short-term indicators
    else:
        return 60  # Default fallback

def extract_features_and_labels(stock, data, strategy, feature_window_length=30, delay=2):
    """
    Extracts features from `feature_window_length` days and labels from the next `feature_window_length` days.
    
    Parameters:
    - stock: str, stock ticker symbol
    - data: pd.DataFrame, stock data (should include 'Close' and 'Volume')
    - strategy: str, trading strategy to evaluate
    - delay: int, cooldown period for trading signals in Trade_Simulator
    
    Returns:
    - X: np.array, extracted feature set (num_samples x num_features x num_days)
    - y: np.array, binary labels (1 = profitable, 0 = not profitable)
    """
    lookback_days = get_lookback_days(strategy)
    window_size = feature_window_length

    X, y = [], []
    # Iterate over the data to create feature and label windows
    for start in range(0, len(data) - lookback_days-window_size, 10):
        # Extract the data window for feature extraction
        feature_window = data.iloc[start:start + lookback_days + window_size]

        # Generate trading signals and indicators
        long_signal, short_signal, indicators = signal_generation(stock, feature_window, strategy)
        indicators = np.array(indicators)[:, -window_size:]  # Keep only the last `window_size` elements

        # Normalize the closing prices
        price_scaler = StandardScaler()
        normalized_price = price_scaler.fit_transform(
            data.iloc[start + lookback_days:start + lookback_days + window_size]["Close"].values.reshape(-1, 1)
        ).flatten()

        # Normalize the indicators
        indicator_scaler = StandardScaler()
        normalized_indicators = indicator_scaler.fit_transform(indicators.T).T

        # Combine normalized price and indicators
        combined_features = np.vstack([normalized_price, normalized_indicators])

        # Simulate trading to determine profitability
        trade_log = Trade_Simulator(
            stock, feature_window, strategy, stop_loss=False, delay=delay, log=True, plot=False, start_trade=lookback_days
        )

        # If no trades were made, label as not profitable
        if trade_log is None or trade_log.empty:
            X.append(combined_features)
            y.append(0)
            continue

        # Determine if the strategy was profitable
        final_capital = trade_log.iloc[-1]["Final Capital"]
        is_profitable = 1 if final_capital > 10000*1.05 else 0

        # Append features and label to the dataset
        X.append(combined_features)
        y.append(is_profitable)
    return np.array(X), np.array(y)

