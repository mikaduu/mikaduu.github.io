import mysql.connector

# 数据库配置
config = {
    'user': 'root',
    'password': 'jjji99997777',
    'host': 'localhost',
    'raise_on_warnings': True
}

# 初始化连接和游标变量
conn = None
cursor = None

# 连接到 MySQL 服务器
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # 读取并执行 .sql 文件中的 SQL 语句
    with open('db.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
        for result in cursor.execute(sql_script, multi=True):
            if result.with_rows:
                result.fetchall()

    # 提交事务
    conn.commit()
    print("Database and tables created successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

except UnicodeDecodeError as ude:
    print(f"UnicodeDecodeError: {ude}")

finally:
    if conn and conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed.")