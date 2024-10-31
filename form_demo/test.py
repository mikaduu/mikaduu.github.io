import pymysql

conn=pymysql.connect(host='localhost',port=3306,
                     user='root',passwd='jjji99997777',
                     database='user',charset='utf8')

def con_my_sql(sql_code):
    try:
        conn.ping(reconnect=True)
        print(sql_code)
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_code)
        conn.commit()
        cursor.close()
        return cursor
    except pymysql. MySQLError as err_message:
        conn.rollback()
        conn.close()
        return type(err_message),err_message

username='mikadu'
password="123456"
e_mail="123@123"
code="INSERT INTO `users` (`username`, `password`,`email`) VALUES ('%s', '%s','%s')"%(username,password,e_mail)
print(con_my_sql(code))