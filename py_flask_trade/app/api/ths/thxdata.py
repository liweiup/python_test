import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_ths_data():
    # 同花顺股票列表页面URL
    url = "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/1/ajax/1/"
    # 发送HTTP请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    # 提取数据
    table = soup.find('table', class_='m-table m-pager-table')
    if table is None:
        print("未找到目标表格。检查页面结构或网络连接。")
        print("页面内容:", response.text[:500])  # 打印页面前500个字符以进行调试
        return

    rows = table.find_all('tr')
    
    data = []
    for row in rows[1:]:  # 跳过表头
        cols = row.find_all('td')
        stock_data = {
            '代码': cols[1].text.strip(),
            '名称': cols[2].text.strip(),
            '现价': cols[3].text.strip(),
            '涨跌幅': cols[4].text.strip(),
            '涨跌': cols[5].text.strip(),
            '涨速': cols[6].text.strip(),
            '换手': cols[7].text.strip(),
            '量比': cols[8].text.strip(),
            '振幅': cols[9].text.strip(),
            '成交额': cols[10].text.strip(),
            '流通股': cols[11].text.strip(),
            '流通市值': cols[12].text.strip(),
            '市盈率': cols[13].text.strip()
        }
        data.append(stock_data)
    
    # 将数据转换为DataFrame
    df = pd.DataFrame(data)
    
    # 保存为CSV文件
    df.to_csv('ths_stock_data.csv', index=False, encoding='utf-8-sig')
    
    print("数据已保存到 ths_stock_data.csv")

if __name__ == "__main__":
    crawl_ths_data()
