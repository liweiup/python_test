import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StockAnalyzer:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.download_data()

    def download_data(self):
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        print(data)
        data.index = pd.to_datetime(data.index, errors='coerce')
        if data.empty:
            logging.error("No valid data available after removing NaN values.")
            raise ValueError("No valid data available")
        return data

    def is_sideways(self, bb_width_threshold=0.25, price_range_threshold=0.05, period=20, recent_days=3, rise_threshold=0.1):
        data = self.data
        data['MA'] = data['Close'].rolling(window=period).mean()
        data['BB_Upper'] = data['MA'] + 2 * data['Close'].rolling(window=period).std()
        data['BB_Lower'] = data['MA'] - 2 * data['Close'].rolling(window=period).std()
        data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['MA']
        data['Price_Range'] = (data['High'] - data['Low']) / data['MA']
        data['Recent_Rise'] = (data['Close'] / data['Close'].shift(recent_days) - 1)
        is_sideways = (data['BB_Width'] < bb_width_threshold) & ((data['Price_Range'] < price_range_threshold) & (data['Recent_Rise'].abs() <= rise_threshold))
        logging.info(f"BB_Width range: {data['BB_Width'].min()} to {data['BB_Width'].max()}")
        logging.info(f"Price_Range range: {data['Price_Range'].min()} to {data['Price_Range'].max()}")
        logging.info(f"Recent_Rise range: {data['Recent_Rise'].min()} to {data['Recent_Rise'].max()}")
        logging.info(f"Number of sideways periods: {is_sideways.sum()}")
        self.data['IsSideways'] = is_sideways
        return is_sideways

    def detect_trend_realtime_improved(self, price_change_threshold=0.05, days_to_check=5):
        data = self.data
        data['Trend'] = 0
        for i in range(1, len(data) - days_to_check + 1):
            if data['IsSideways'].iloc[i-1] and not data['IsSideways'].iloc[i]:
                start_price = data['Close'].iloc[i-1]
                cumulative_price_change = 0
                for j in range(days_to_check):
                    current_price = data['Close'].iloc[i+j]
                    price_change = (current_price - start_price) / start_price
                    cumulative_price_change += price_change
                    if cumulative_price_change >= price_change_threshold:
                        trend_direction = 1
                        break
                    elif cumulative_price_change <= -price_change_threshold:
                        trend_direction = -1
                        break
                else:
                    trend_direction = 0
                
                if trend_direction != 0:
                    for k in range(days_to_check):
                        data.loc[data.index[i+k], 'Trend'] = (k + 1) * trend_direction

        data.loc[data['IsSideways'], 'Trend'] = 0

        for i in range(1, len(data)):
            if not data['IsSideways'].iloc[i] and data['Trend'].iloc[i] == 0:
                data.loc[data.index[i], 'Trend'] = data['Trend'].iloc[i-1] + (1 if data['Close'].iloc[i] > data['Close'].iloc[i-1] else -1)

        return data

    def volume_surge(self, window=5, threshold=1.5):
        data = self.data
        recent_volume = data['Volume'].rolling(window=window).mean()
        previous_volume = data['Volume'].shift(window).rolling(window=window).mean()
        volume_surge = recent_volume > previous_volume * threshold
        self.data['Volume_Surge'] = volume_surge
        return volume_surge

    def plot(self, save_path=None):
        data = self.data
        data['Sideways_Marker'] = data['IsSideways'].apply(lambda x: np.nan if not x else 1) * data['Close']
        data['Trend_Up'] = data.apply(lambda row: row['Close'] if row['Trend'] == 1 else np.nan, axis=1)
        data['Trend_Down'] = data.apply(lambda row: row['Close'] if row['Trend'] == -1 else np.nan, axis=1)
        data['Trend_Up_Strong'] = data.apply(lambda row: row['Close'] if row['Trend'] > 1 else np.nan, axis=1)
        data['Trend_Down_Strong'] = data.apply(lambda row: row['Close'] if row['Trend'] < -1 else np.nan, axis=1)

        mc = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')
        s = mpf.make_mpf_style(marketcolors=mc)
        apds = [
            mpf.make_addplot(data['MA'], color='blue'),
            mpf.make_addplot(data['BB_Upper'], color='gray'),
            mpf.make_addplot(data['BB_Lower'], color='gray'),
        ]
        if not data['Sideways_Marker'].isna().all():
            apds.append(mpf.make_addplot(data['Sideways_Marker'], type='scatter', markersize=10, marker='o', color='purple'))
        if not data['Trend_Up'].isna().all():
            apds.append(mpf.make_addplot(data['Trend_Up'], type='scatter', markersize=20, marker='^', color='red'))
        if not data['Trend_Down'].isna().all():
            apds.append(mpf.make_addplot(data['Trend_Down'], type='scatter', markersize=20, marker='v', color='green'))
        if not data['Trend_Up_Strong'].isna().all():
            apds.append(mpf.make_addplot(data['Trend_Up_Strong'], type='scatter', markersize=20, marker='^', color='darkred'))
        if not data['Trend_Down_Strong'].isna().all():
            apds.append(mpf.make_addplot(data['Trend_Down_Strong'], type='scatter', markersize=20, marker='v', color='darkgreen'))

        fig, axlist = mpf.plot(data, type='candle', style=s, addplot=apds,
                               title=f'{self.ticker} Bollinger Bands and Sideways Detection',
                               volume=True, figsize=(12, 8), returnfig=True)
        if save_path:
            fig.savefig(save_path)
            logging.info(f"Plot saved to {save_path}")


    def save_to_csv(self, filepath):
        self.data.to_csv(filepath, index=True)

    def print_trends(self):
        data = self.data
        print("All periods and trends:")
        for index, row in data.iterrows():
            if row['IsSideways']:
                trend_str = "Sideways"
            elif row['Trend'] == 1:
                trend_str = "Up"
            elif row['Trend'] == -1:
                trend_str = "Down"
            else:
                trend_str = "No Trend"
            print(f"{index.date()}: {trend_str}")

# Example usage
if __name__ == "__main__":
    analyzer = StockAnalyzer(ticker='600550.SS', start_date='2024-04-01', end_date='2024-09-04')
    analyzer.volume_surge()
    analyzer.is_sideways()
    analyzer.detect_trend_realtime_improved()
    analyzer.plot()
    analyzer.print_trends()
    analyzer.save_to_csv('./views/output_data.csv')