import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from signal_generator import signal_generation
from plot_generation import plot_generator

def Trade_Simulator(stock, data, strategy, stop_loss=False, delay=2,log=False,plot=True,start_trade=0):
    """
    A trading simulator supporting multiple strategies with a cooldown period and proper capital tracking.
    
    Parameters:
    - stock: str, the stock ticker (column name in `data`)
    - data: pd.DataFrame, closing prices
    - strategy: str, trading strategy name
    - stop_loss: bool, whether to use stop-loss exits
    - delay: int, number of days to wait before flipping long/short
    
    Returns:
    - trade_log_df: pd.DataFrame, trade execution log
    """
    long_signal, short_signal, curve_data = signal_generation(stock, data, strategy)
    data = data["Close"]

    initial_capital = 10000.0
    capital = initial_capital  # Cash balance
    position_size = 100
    capital_over_time = []  # Tracks available cash
    equity_over_time = []  # Tracks total portfolio value (cash + open positions)
    in_position = False
    trade_type = None
    trade_log = []
    shares = 0
    cooldown_counter = 0  # Tracks the delay period

    for i in range(start_trade, len(data)):
        current_price = data[stock].iloc[i]

        if cooldown_counter > 0:
            cooldown_counter -= 1  # Reduce cooldown each day
            capital_over_time.append(capital)
            equity_over_time.append(capital + shares * current_price)  # Update total portfolio value
            continue  # Skip trade execution during cooldown

        if in_position:
            stop_loss_price = 0.95 * current_price if trade_type == "long" else 1.05 * current_price

            # Stop-Loss Exit
            if stop_loss and ((trade_type == "long" and current_price < stop_loss_price) or 
                              (trade_type == "short" and current_price > stop_loss_price)):
                capital += shares * current_price  # Close position at stop-loss
                trade_log.append({"Date": data.index[i], "Type": "STOP-LOSS EXIT", "Exit Price": current_price, "Final Capital": capital})
                in_position = False
                trade_type = None
                shares = 0
                cooldown_counter = delay  # Start cooldown period

            # Regular Exit (Signal Flipped)
            elif (trade_type == "long" and short_signal.iloc[i]) or (trade_type == "short" and long_signal.iloc[i]):
                capital += shares * current_price  # Close position
                trade_log.append({"Date": data.index[i], "Type": "EXIT", "Exit Price": current_price, "Final Capital": capital})
                in_position = False
                trade_type = None
                shares = 0
                cooldown_counter = delay  # Start cooldown period

        else:
            # Only enter new positions if not in cooldown period
            if cooldown_counter == 0:
                if long_signal.iloc[i]:
                    shares = position_size
                    capital -= shares * current_price  # Buy shares (reduce cash)
                    in_position = True
                    trade_type = "long"
                    trade_log.append({"Date": data.index[i], "Type": "LONG", "Remaining Capital": capital})

                elif short_signal.iloc[i]:
                    shares = -position_size
                    capital += abs(shares) * current_price  # Receive cash for selling short
                    in_position = True
                    trade_type = "short"
                    trade_log.append({"Date": data.index[i], "Type": "SHORT", "Remaining Capital": capital})

        capital_over_time.append(capital)
        equity_over_time.append(capital + shares * current_price)  # Portfolio value = Cash + Open Positions
    if in_position:
        final_price = data[stock].iloc[-1]  # Get final stock price
        capital += shares * final_price  # Close position at last available price
        trade_log.append({"Date": data.index[-1], "Type": "FINAL EXIT", "Exit Price": final_price, "Final Capital": capital})
    trade_log_df = pd.DataFrame(trade_log)

    # Generate trade plots
    if plot:
        plot_generator(stock, data, curve_data, strategy, trade_log_df, equity_over_time)
    if log==False:
        return
    else:
        return trade_log_df  # Return trade log for analysis
