# Algorithmic Trading Strategies for Stock Analysis

This repository contains code that applies various traditional trading strategies to historical stock data and enhances them using machine learning. The project demonstrates how to generate trading signals using technical indicators, simulate trades, and evaluate performance—both through backtesting and predictive modeling.

## Project Overview

This project performs the following steps:

- **Data Acquisition:**  
  Download historical stock data (closing prices and volume) from Yahoo Finance using the `yfinance` API.

- **Signal Generation:**  
  Compute technical indicators and generate trading signals for different strategies.

- **Trading Strategies:**  
  Implement various strategies including:
  - **Momentum:** Uses moving averages to determine trend direction.
  - **Mean Reversion with Bollinger Bands:** Uses a 100-day rolling mean and standard deviation to define overbought/oversold conditions.
  - **Breakout:** Trades based on recent 20-day highs and lows.
  - **RSI-based:** Generates signals based on the Relative Strength Index.
  - **MACD-based:** Uses the Moving Average Convergence/Divergence indicator.
  - **VWAP-based:** Uses a Volume Weighted Average Price over a 50-day rolling window.

- **Trade Simulation:**  
  Simulate trading based on the generated signals, visualizing trade entries, exits, and portfolio performance.

- **Visualization:**  
  Plot trade signals, technical indicators, and portfolio value over time for clear performance insights.
  
- **Machine Learning Forecasting:**  
  For each strategy, a dedicated neural network was trained to forecast the profitability of applying the strategy under current market conditions. This predictive layer helps prioritize strategies based on expected returns, achieving:
  - ~70% overall classification accuracy,
  - ~90% precision, the accuracy was driven down by high FNR. In this context we desire high precision, even we risk missing some opportunities for porift.
