import yfinance as yf
import pandas as pd
from datetime import datetime

def download_stock_data(symbol, period, interval):
    return yf.download(tickers=symbol, period=period, interval=interval)

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
    processed_data = process_data_frame(data)
    save_to_csv(processed_data, filename)

if __name__ == '__main__':
    # 現在の日付を取得してファイル名を作成
    today = datetime.today().strftime('%Y%m%d')
    filename = f"FLOW_{today}.csv"
    csv_main("FLOW-USD", "1y", "1h", filename)
