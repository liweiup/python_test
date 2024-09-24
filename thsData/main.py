import sys
import os

# 将项目根目录添加到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from scripts.search_stock import search_stock
from analyzer.stock_analyzer_byboll import StockAnalyzer
def test_stock_analyzer():
    analyzer = StockAnalyzer(ticker='600550.SS', start_date='2024-04-01', end_date='2024-09-25')
    analyzer.volume_surge()
    analyzer.is_sideways()
    analyzer.detect_trend_realtime_improved()
    analyzer.plot(save_path=f"/usr/local/www/python_test/thsData/views/{analyzer.ticker}_output_data.png")
    analyzer.print_trends()
    analyzer.save_to_csv(f"/usr/local/www/python_test/thsData/views/{analyzer.ticker}_output_data.csv")
def main():
    test_stock_analyzer()
    
if __name__ == "__main__":
    main()