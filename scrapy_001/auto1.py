from dbfread import DBF

# 打开DBF文件
dbf_file = DBF('/Users/bird/Downloads/NNC_DATA02_08.DBF',encoding='latin1')

# 遍历DBF文件中的所有记录
for record in dbf_file:
    print(record)
    exit
