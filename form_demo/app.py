from flask import Flask, render_template, request,jsonify,session,redirect,url_for,flash
from functools import wraps
from werkzeug.utils import secure_filename
import pymysql

app = Flask(__name__)
app.secret_key = 'my minecraft community'
conn = pymysql.connect(host='localhost', port=3306,
                       user='root', passwd='jjji99997777',
                       database='user', charset='utf8')


def con_my_sql(sql_code, params=None):
    try:
        conn.ping(reconnect=True)
        print(sql_code)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if params:
            cursor.execute(sql_code, params)
        else:
            cursor.execute(sql_code)
        conn.commit()
        
        return cursor
    except pymysql.MySQLError as err_message:
        conn.rollback()
        return None, type(err_message), err_message

#登录验证装饰器，确保用户登录后才能进行一些操作
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))  # 如果未登录，则重定向到登录页面
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    username = session.get('username')
    user_info=None
    if username:
        code = "SELECT * FROM users WHERE username=%s"
        cursor_ans = con_my_sql(code, (username,))
        cursor_select = cursor_ans.fetchall()
        cursor_ans.close()
        user_info = cursor_select[0]
    return render_template('index.html', username=username,user_info=user_info)

@app.route('/user/<int:id>')
@login_required
def user(id):
    username = session.get('username')
    code = "SELECT * FROM users WHERE username=%s"
    cursor_ans = con_my_sql(code, (username,))
    cursor_select = cursor_ans.fetchall()
    cursor_ans.close()
    user_info = cursor_select[0]
    return render_template('user.html', username=username,user_info=user_info,id=id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        psw = request.form.get('password')
        code = "SELECT * FROM users WHERE username=%s"
        cursor_ans = con_my_sql(code, (name,))
        if cursor_ans is None:
            flash("数据库查询失败")
            return render_template('login.html')
        cursor_select = cursor_ans.fetchall()
        cursor_ans.close()
        if len(cursor_select) > 0:
            user = cursor_select[0]
            if psw == user["password"]:
                session['username'] = name

                flash("登录成功")
                return redirect(url_for('index'))
            else:
                 flash("密码错误")
                 return render_template('login.html')
        else:
             flash("用户不存在")
             return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        psw1 = request.form.get('password')
        psw2 = request.form.get('confirm_password')
        email = request.form.get('email')
        if psw1 != psw2:
            flash("两次密码不一致")
            return render_template('register.html')
        code = "SELECT * FROM users WHERE username=%s"
        cursor_ans = con_my_sql(code, (name,))
        if cursor_ans is None:  # 修改部分：检查游标是否为 None
            flash("数据库查询失败")
            return render_template('register.html')
        cursor_select=cursor_ans.fetchall()
        cursor_ans.close()
        if len(cursor_select) > 0:
            flash("用户已存在")
            return render_template('register.html')
        else:
            code = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            result=con_my_sql(code, (name, psw1, email))
            if result is None:  # 修改部分：检查插入操作是否成功
                flash("注册失败")
                return render_template('register.html')
            session['username'] = name
            flash("注册成功")
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # 移除 username 的会话
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
    # name='123'
    # password='123'
    # email='123@123'
    # code = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    # result = con_my_sql(code, (name, password, email))
