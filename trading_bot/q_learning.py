import numpy as np
import random

def q_learning_stock_selection(stocks, budget, epochs=1000):
    """
    Q-learning algorithm for stock selection.
    - stocks: List of stocks with risk & volatility.
    - budget: Amount available to trade.
    - epochs: Training iterations.
    
    Returns: (best_stock, invest_amount)
    """
    num_stocks = len(stocks)
    Q_table = np.zeros((num_stocks, budget + 1))

    for _ in range(epochs):
        state = budget  # Start with full budget
        for i, stock in enumerate(stocks):
            action = random.randint(0, state)  # Choose an amount to invest
            reward = action * (stock["volatility"] / 100)  # Simulate profit potential
            Q_table[i, state] = max(Q_table[i, state], reward)
            state -= action  # Reduce available budget

    print ("Q_table: ", Q_table)
    best_stock_index = np.argmax(Q_table[:, budget])
    best_stock = stocks[best_stock_index]
    invest_amount = budget // (best_stock_index + 1) if best_stock_index > 0 else budget

    return best_stock, invest_amount
