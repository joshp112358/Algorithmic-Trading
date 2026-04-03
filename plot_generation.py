import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def plot_generator(stock,data,curve_data,strategy,trade_log_df,capital_over_time):
    if strategy == "rsi":
        strategy_name="RSI"
        plt.figure(figsize=(12,6))
        plt.plot(data.index, curve_data[0], color='red', linestyle='--', label='RSI')
        plt.title("RSI")
        plt.legend()
        plt.show()
    plt.figure(figsize=(12,6))
    plt.plot(data.index, data[stock], label=f"Closing Price of {stock}", color="black")
    if strategy == "momentum":
        strategy_name="Momentum"
        plt.plot(data.index, curve_data[0], color='red', linestyle='--', label='Short-Term MA')
        plt.plot(data.index, curve_data[1], color='green', linestyle='--', label='Long-Term MA')
    elif strategy == "mean_reversion":
        strategy_name="Mean Reversion"
        plt.plot(data.index, curve_data[0], color='red', linestyle='--', label='Upper Bollinger Band')
        plt.plot(data.index, curve_data[1], color='green', linestyle='--', label='Lower Bollinger Band')
        plt.plot(data.index, curve_data[2], color='blue', linestyle='--', label='Rolling Mean')
    if strategy == "breakout":
        strategy_name="Breakout"
        plt.plot(data.index, curve_data[0], color='red', linestyle='--', label='Rolling Max Price')
        plt.plot(data.index, curve_data[1], color='green', linestyle='--', label='Rolling Min Price')
    if strategy == "macd":
        strategy_name="Moving Average Convergence Divergence"
        plt.plot(data.index, curve_data[0], color='red', linestyle='--', label='Short Term Exponential Moving Average')
        plt.plot(data.index, curve_data[1], color='green', linestyle='--', label='Long Term Exponential Moving Average')
    if strategy == "vwap":
        strategy_name="Volume-Weighted Moving Average"
        plt.plot(data.index, curve_data[0], color='red', linestyle='--', label='Volume-Weighted Moving Average')
    for _, trade in trade_log_df.iterrows():
        if "LONG" in trade["Type"]:
            plt.scatter(trade["Date"], data.loc[trade["Date"], stock], marker="^", color="green", s=100)
        elif "SHORT" in trade["Type"]:
            plt.scatter(trade["Date"], data.loc[trade["Date"], stock], marker="v", color="red", s=100)
        elif "EXIT" in trade["Type"]:
            plt.scatter(trade["Date"], data.loc[trade["Date"], stock], marker="o", color="blue", s=70)
    plt.scatter([], [], marker="^", color="green", s=100, label="Long Signal")
    plt.scatter([], [], marker="v", color="red", s=100, label="Short Signal")
    plt.scatter([], [], marker="o", color="blue", s=70, label="Exit Signal")

    plt.legend()
    plt.title(f"{strategy_name} Strategy for {stock}")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.show()
    # Capital Over Time
    plt.figure(figsize=(12,6))
    plt.plot(capital_over_time, label="Capital over time", color="black")
    plt.title("Strategy Equity Curve")
    plt.legend()
    plt.show()