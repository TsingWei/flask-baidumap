from flask import Flask, request, redirect, url_for, render_template, flash, json, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, query_user
from geoServer import SQLConnection
import socket,threading,pickle
import collections

app = Flask(__name__)
app.secret_key = '1234567'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)


udpListener = collections.deque()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 12345))
# sql = SQLConnection()


@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user

# 位置服务器
@app.route('/map_server',methods=['GET','POST'])#路由
def map_server():
    if len(udpListener) >0 :
        point = udpListener.popleft()
        return jsonify(new=True,x=point[0],y=point[1])
    else:
        return jsonify(new=False)

# 初始化位置服务器，向数据库询问最新的10个点
@app.route('/init_server',methods=['GET','POST'])#路由
def init_server():
        
    return jsonify(new=False)

@app.route('/',methods=['GET','POST'])
@login_required
def index():
    username = 'Logged in as: %s' % current_user.get_id()
    return render_template('map.html')

# 登陆页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userid')
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:

            curr_user = User()
            curr_user.id = user_id

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)

            return redirect(url_for('index'))

        flash('Wrong username or password!')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'


def udpServer():
    while True:
        data, addr = s.recvfrom(1024)
        data = pickle.loads(data)
        udpListener.append(tuple(data))



if __name__ == '__main__':
    t = threading.Thread(target=udpServer)
    t.daemon = True
    t.start()
    app.run(debug=True,use_reloader=False, port=10101)
    
