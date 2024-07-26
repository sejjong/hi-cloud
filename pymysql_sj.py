import pymysql

host = "database-1.cpeweyygc27i.ap-southeast-2.rds.amazonaws.com"
user = "admin"
password = "sejong123!"
name = 'mydb'
table = 'mytable'

connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    db = name
)

try:
    with connection.cursor() as cursor:
        insert_data = [
            ('3', 'sejong_jeong', 'tpwhd3004@vm.ac.kr')
        ]
        
        sql = f"INSERT INTO {table} (id, name, email) VALUES (%s, %s, %s)"
        
        cursor.executemany(sql, insert_data)
        
        connection.commit()
        
        print("데이터 추가 완료")
        
finally:
    connection.close()