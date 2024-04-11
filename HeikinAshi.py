import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
# Set a backend for matplotlib
plt.switch_backend('TkAgg')

def calculate_heikin_ashi(df):
    ha_df = pd.DataFrame(index=df.index)
    ha_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha_df['Open'] = ((df['Open'].shift(1) + df['Close'].shift(1)) / 2).fillna(df['Open'])
    ha_df['High'] = ha_df[['Open', 'Close']].join(df['High']).max(axis=1)
    ha_df['Low'] = ha_df[['Open', 'Close']].join(df['Low']).min(axis=1)
    return ha_df

def plot_heikin_ashi(ha_df, title='Heikin Ashi Chart'):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(len(ha_df)):
        color = 'green' if ha_df['Open'][i] < ha_df['Close'][i] else 'red'
        ax.vlines(x=i, ymin=ha_df['Low'][i], ymax=ha_df['High'][i], color=color, linewidth=2)
        ax.vlines(x=i, ymin=min(ha_df['Open'][i], ha_df['Close'][i]), ymax=max(ha_df['Open'][i], ha_df['Close'][i]), color=color, linewidth=4)
    
    ax.set_xticks(range(0, len(ha_df.index), max(1, len(ha_df.index) // 10)))
    ax.set_xticklabels(ha_df.index[::max(1, len(ha_df.index) // 10)].date, rotation=45)
    ax.set_title(title)

    plt.show()

# Replace 'AAPL' with the ticker you're interested in and adjust the period as needed
ticker = 'AAPL'
data = yf.download(ticker, start='2023-01-01', end='2023-04-01')

# Calculate Heikin Ashi
ha_data = calculate_heikin_ashi(data)

# Plot
plot_heikin_ashi(ha_data, title=f'Heikin Ashi Chart for {ticker}')
