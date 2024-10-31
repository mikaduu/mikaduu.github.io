from flask import Flask, render_template, request,jsonify,session,redirect,url_for,flash
from functools import wraps
from werkzeug.utils import secure_filename
import pymysql
import os
import time

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
    code = "SELECT * FROM users WHERE id=%s"
    cursor_ans = con_my_sql(code, (id,))
    cursor_select = cursor_ans.fetchall()
    cursor_ans.close()
    user_info2 = cursor_select[0]
    return render_template('user.html', username=username,user_info=user_info,id=id,user_info2=user_info2)

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

                #flash("登录成功")
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
            #flash("注册成功")
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # 移除 username 的会话
    return redirect('/')

@app.route('/edit_user', methods=['POST'])
@login_required
def edit_user():
    username = session.get('username')
    new_username = request.json.get('username')
    new_email = request.json.get('email')
    
    # 检查新用户名是否已经存在
    if new_username and new_username != username:
        code = "SELECT * FROM users WHERE username=%s"
        cursor_ans = con_my_sql(code, (new_username,))
        cursor_select = cursor_ans.fetchall()
        cursor_ans.close()
        if cursor_select:
            return jsonify({"message": "用户名已存在！"}), 400  # 用户名已存在，拒绝修改

    # 更新用户名和邮箱
    code = "UPDATE users SET username=%s, email=%s WHERE username=%s"
    result = con_my_sql(code, (new_username, new_email, username))

    if result:
        session['username'] = new_username if new_username else username  # 更新会话中的用户名
        return jsonify({"message": "用户信息已更新！"})
    else:
        return jsonify({"message": "更新失败！"}), 400

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    username = session.get('username')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    # 查询用户当前的密码
    code = "SELECT * FROM users WHERE username=%s"
    cursor_ans = con_my_sql(code, (username,))
    cursor_select = cursor_ans.fetchall()
    cursor_ans.close()

    if cursor_select and cursor_select[0]['password'] == old_password:
        # 更新密码
        update_code = "UPDATE users SET password=%s WHERE username=%s"
        result = con_my_sql(update_code, (new_password, username))
        if result:
            return jsonify({"message": "密码已修改！"})
        else:
            return jsonify({"message": "修改密码失败！"}), 400
    else:
        return jsonify({"message": "旧密码不正确！"}), 400


@app.route('/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({"message": "未选择文件！"}), 400

    file = request.files['avatar']
    username = session.get('username')

    code = "SELECT id FROM users WHERE username=%s"
    cursor_ans = con_my_sql(code, (username,))
    cursor_select = cursor_ans.fetchall()
    cursor_ans.close()

    user_id = cursor_select[0]['id'] if cursor_select else None

    if file and user_id:
        filename = secure_filename(file.filename)
        # 修改文件名为 "用户ID_时间戳.扩展名"
        new_filename = f"{user_id}_{int(time.time())}.{filename.rsplit('.', 1)[-1]}"
        avatar_path = os.path.join('static/images/', new_filename)
        file.save(avatar_path)
        relative_path = f"images/{new_filename}"
        # 更新数据库中的头像路径
        code = "UPDATE users SET avatar_url=%s WHERE id=%s"
        result = con_my_sql(code, (relative_path, user_id))
        if result:
            return jsonify({"message": "头像已上传！"})
        else:
            return jsonify({"message": "头像上传失败！"}), 400

    return jsonify({"message": "上传失败！"}), 400

@app.route('/search_user', methods=['POST'])
@login_required
def search_user():
    username = request.json.get('username')

    # 查询用户
    code = "SELECT * FROM users WHERE username=%s"
    cursor_ans = con_my_sql(code, (username,))
    cursor_select = cursor_ans.fetchall()
    cursor_ans.close()

    if cursor_select:
        user_id = cursor_select[0]['id']  # 获取找到的用户 ID
        return jsonify({'status':1,'user_id': user_id,"message":"即将跳转到指定用户的主页"}), 200 
    else:
        return jsonify({'status':0,'message': '用户未找到'}), 404 


if __name__ == '__main__':
    app.run(debug=True)
    # name='123'
    # password='123'
    # email='123@123'
    # code = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    # result = con_my_sql(code, (name, password, email))
