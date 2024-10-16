from common.mysqlCon import MySQLConnector
from common.redisUtils import RedisUtils
from analyzer.stock_analyzer import StockAnalyzer
def search_stock(c_date,phase_length=10):
    # SQL query
    sql_query = """
    SELECT tab_name,
           stock_name,
           stock_code,
           price,
           change_percent,
           c_date
    FROM ths_sentiment_stock tss
    WHERE c_date = %s
    limit 30
    """
    try:
        with MySQLConnector() as db:
            results = db.execute_query(sql_query,(c_date,))
            print(results)
            print(f"Query executed. Number of results: {len(results)}")
            if not results:
                print("No results found for the given date.")
                return
            analyzer = StockAnalyzer(price_threshold=0.3, days_threshold=30)
            # Iterate through the results
            for row in results:
                # 获取K线数据
                csql_query = """
                SELECT close, c_date 
                FROM dd_day_kline 
                WHERE stock_code LIKE %s AND c_date <= %s 
                ORDER BY c_date DESC 
                LIMIT %s
                """
                stock_code_pattern = f"%{row['stock_code']}"
                kline_results = db.execute_query(csql_query, (stock_code_pattern, row['c_date'], phase_length * 3))
                if kline_results and len(kline_results) >= phase_length * 3:
                    # 提取 close 价格并反转列表（使最早的日期在前）
                    close_prices = [float(result['close']) for result in reversed(kline_results)]
                    # 分析股票
                    analysis_result = analyzer.analyze_stock(close_prices, phase_length)

                    print(f"Stock Analysis:{row['stock_name']}")
                    print(f"  Current is sideways: {analysis_result['current_is_sideways']}")
                    print(f"  Current fluctuation: {analysis_result['current_fluctuation']:.2%}")
                    print(f"  Overall trend: {analysis_result['overall_trend']:.4f}")
                    print(f"  Has sideways->down->up pattern: {analysis_result['has_sideways_down_up_pattern']}")
                    print(f"  Pattern description: {analysis_result['pattern_description']}")
                    print(f"  Analysis: {analysis_result['analysis']}")

                    print("K-line data (last 5 days):")
                    for kline_row in kline_results[:5]:  # 只打印最近5天的数据
                        print(f"  Date: {kline_row['c_date']}, Close: {kline_row['close']}")
                else:
                    print(f"Insufficient K-line data for analysis. Found {len(kline_results) if kline_results else 0} data points, need at least {phase_length * 3}.")
                print("-" * 50)

                # 后30天数据
                # csql_query = """
                # select open,high,low,close,c_date from dd_day_kline where stock_code like %s and c_date > %s order by c_date asc limit 30
                # """
                # kline_results = db.execute_query(csql_query, (stock_code_pattern,row['c_date']))
                # if kline_results:
                #     print("K-line data:")
                #     for kline_row in kline_results:
                #         print(f"  Date: {kline_row['c_date']}, Open: {kline_row['open']}, High: {kline_row['high']}, Low: {kline_row['low']}, Close: {kline_row['close']}")
                # else:
                #     print("No K-line data found for this stock."+row['stock_code'])
                
            # print(f"Stock Name: {row['stock_name']}")
            # print(f"Tab Name: {row['tab_name']}")
            # print(f"Price: {row['price']}")
            # print(f"Change Percent: {row['change_percent']}")
            # print(f"Date: {row['c_date']}")
    except Exception as e:
        print(f"An error occurred: {e}")
