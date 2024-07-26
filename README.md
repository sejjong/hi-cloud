# April to-do

1. 회원가입

2. RDS DB 생성

https://velog.io/@squarebird/AWS-RDS

3. 테이블구성

![image](https://github.com/user-attachments/assets/d88f6010-a212-4386-b37a-b6a4ce1af62f)

4. pymysql 로 데이터 추가
![image](https://github.com/user-attachments/assets/9cc3bc39-d7ba-4930-b35d-6702892eb164)

5. workbench 확인
![image](https://github.com/user-attachments/assets/f900aafc-0f51-4cab-ad10-de42448710e4)

6.vm 연결 (하기전에 ssh 인바운드 규칙 추가)
![image](https://github.com/user-attachments/assets/a23e896b-a224-4693-a7bc-c649f2cf7418)

7. vm 에서 데이터 추가
![image](https://github.com/user-attachments/assets/724fdc09-0068-497f-a7ec-2a691355c478)

8. venv 에서 데이터 추가
![image](https://github.com/user-attachments/assets/1b4e7fd7-7148-453b-a579-430cb9b26324)

```python
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
```

# June to-do
