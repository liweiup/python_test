import sys
import os
# 将项目根目录添加到 Python 路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from scripts.search_stock import search_stock
from analyzer.stock_analyzer_byboll import StockAnalyzer
def test_stock_analyzer():
    print(123)
    analyzer = StockAnalyzer(ticker='600550.SS', start_date='2024-04-01', end_date='2024-09-25')
    print(1234)
    analyzer.volume_surge()
    analyzer.is_sideways()
    analyzer.detect_trend_realtime_improved()
    # analyzer.plot()
    project_root = find_project_root()
    analyzer.plot(save_path=f"{project_root}/views/{analyzer.ticker}_output_data.png")
    analyzer.print_trends()
    analyzer.save_to_csv(f"{project_root}/views/{analyzer.ticker}_output_data.csv")

def find_project_root(filename="requirements.txt"):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while current_dir != os.path.abspath(os.sep):
        if filename in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    raise FileNotFoundError(f"Could not find {filename} in any parent directory")
def main():
    test_stock_analyzer()
    project_root = find_project_root()
    print(project_root)
if __name__ == "__main__":
    search_stock('2024-09-10')
    # main()