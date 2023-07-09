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
        return yf.download(tickers=symbol, period=period, interval=interval), None
    except Exception as e:
        return None, f"yfinanceエラー： {str(e)}"

def process_data_frame(df, sym):
    if ".T" not in sym:
        df.index += pd.Timedelta(hours=9)

    df['Date'], df['Time'] = df.index.date, df.index.time
    df = df[['Date', 'Time'] + [c for c in df if c not in ['Date', 'Time']]]
    df = df.drop(columns=["Adj Close"]).reset_index(drop=True)
    return df

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

def download_stock_data(symbol, period, interval):
    try:
        return yf.download(tickers=symbol, period=period, interval=interval), None
    except Exception as e:
        return None, f"yfinanceエラー： {str(e)}"

def csv_main(symbol, period, interval, filename):
    data, error_message = download_stock_data(symbol, period, interval)
    if data is None or data.size == 0:
        result_label.config(text="エラーが発生しました。設定値を見直してください")
        #result_label.config(text=error_message)
        return False
    else:
        processed_data = process_data_frame(data, symbol)
        save_to_csv(processed_data, filename)
        result_label.config(text="データをダウンロードしました。")
        return True
def download_data():
    symbol = symbol_entry.get()
    period = period_var.get()
    interval = interval_var.get()  # 変更点

    # 現在の日付を取得してファイル名を作成
    today = datetime.today().strftime('%Y%m%d')
    filename = f"{symbol}_{today}.csv"

    error_message = csv_main(f"{symbol}", period, interval, filename)
    if error_message is True:
        save_input_values(symbol, period, interval)

    #result_label.config(text=error_message)

# GUIの作成
window = tk.Tk()
window.title("株価データダウンローダ")
window.geometry("250x380")

# 空白行の挿入
tk.Label(window, text="").pack()

# 変数の定義と前回の値の読み込み
symbol_var = tk.StringVar()
symbol_label = tk.Label(window, text="■ 通貨(シンボル名)：\n　以下を末尾に加えること\n・仮想通貨：'-USD'\n・日本株：'.T'\n・FX'=X'")
symbol_label.pack()
symbol_entry = tk.Entry(window, textvariable=symbol_var)
symbol_entry.pack()
symbol, _, _ = load_input_values()
symbol_entry.insert(0, symbol)

# 空白行の挿入
tk.Label(window, text="").pack()

# 取得期間の選択肢
period_options = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
# 取得期間の設定
period_var = tk.StringVar()
period_var.set(period_options[0])  # 初期値
period_label = tk.Label(window, text="■ 取得期間 (1y/3mo/1moなど)：")
period_label.pack()
period_optionmenu = tk.OptionMenu(window, period_var, *period_options)
period_optionmenu.pack()

# 前回の値の読み込み
_, period, _ = load_input_values()
period_var.set(period)

# 空白行の挿入
tk.Label(window, text="").pack()

# 取得単位の選択肢
interval_options = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
# 取得単位の設定
interval_var = tk.StringVar()
interval_var.set(interval_options[0])  # 初期値
interval_label = tk.Label(window, text="■ 取得単位 (1d/1h/15mなど)：")
interval_label.pack()
interval_optionmenu = tk.OptionMenu(window, interval_var, *interval_options)
interval_optionmenu.pack()

# 前回の値の読み込み
_, _, interval = load_input_values()
interval_var.set(interval)

# 空白行の挿入
tk.Label(window, text="").pack()

download_button = tk.Button(window, text="データをダウンロード", command=download_data)
download_button.pack()

# 空白行の挿入
tk.Label(window, text="").pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
