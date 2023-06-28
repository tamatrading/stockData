import tkinter as tk
from datetime import datetime
import yfinance as yf
import pandas as pd

def save_input_values(symbol, period, interval):
    with open("input_values.txt", "w") as f:
        f.write(f"{symbol}\n")
        f.write(f"{period}\n")
        f.write(f"{interval}\n")

def load_input_values():
    try:
        with open("input_values.txt", "r") as f:
            symbol = f.readline().strip()
            period = f.readline().strip()
            interval = f.readline().strip()
            return symbol, period, interval
    except FileNotFoundError:
        return "", "", ""

def download_stock_data(symbol, period, interval):
    try:
        return yf.download(tickers=symbol, period=period, interval=interval)
    except Exception as e:
        error_message = f"yfinanceエラー： {str(e)}"
        result_label.config(text=error_message)

def process_data_frame(df):
    df.index += pd.Timedelta(hours=9)
    df['Date'], df['Time'] = df.index.date, df.index.time
    df = df[['Date', 'Time'] + [c for c in df if c not in ['Date', 'Time']]]
    df = df.drop(columns=["Adj Close"]).reset_index(drop=True)
    return df

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

def csv_main(symbol, period, interval, filename):
    data = download_stock_data(symbol, period, interval)
    if data is not None:
        processed_data = process_data_frame(data)
        save_to_csv(processed_data, filename)

def download_data():
    symbol = symbol_entry.get()
    period = period_entry.get()
    interval = interval_entry.get()

    # 現在の日付を取得してファイル名を作成
    today = datetime.today().strftime('%Y%m%d')
    filename = f"{symbol}_{today}.csv"

    csv_main(f"{symbol}-USD", period, interval, filename)
    save_input_values(symbol, period, interval)

    result_label.config(text="データをダウンロードしました。")

# GUIの作成
window = tk.Tk()
window.title("株価データダウンローダ")
window.geometry("300x200")

# 変数の定義と前回の値の読み込み
symbol_var = tk.StringVar()
symbol_label = tk.Label(window, text="通貨(シンボル名)：")
symbol_label.pack()
symbol_entry = tk.Entry(window, textvariable=symbol_var)
symbol_entry.pack()
symbol, _, _ = load_input_values()
symbol_entry.insert(0, symbol)

period_var = tk.StringVar()
period_label = tk.Label(window, text="取得期間(1y/3mo/1moなど)：")
period_label.pack()
period_entry = tk.Entry(window, textvariable=period_var)
period_entry.pack()
_, period, _ = load_input_values()
period_entry.insert(0, period)

interval_var = tk.StringVar()
interval_label = tk.Label(window, text="取得単位(1d/1hなど)：")
interval_label.pack()
interval_entry = tk.Entry(window, textvariable=interval_var)
interval_entry.pack()
_, _, interval = load_input_values()
interval_entry.insert(0, interval)

download_button = tk.Button(window, text="Download", command=download_data)
download_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
