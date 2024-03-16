# app.py
from flask import Flask, render_template, request
from flask import jsonify
import inspect
import ctypes
from main import OnlineCompetitionMonitor

app = Flask(__name__)

email = "1@q.com"
user_to_track = "1"

monitor = OnlineCompetitionMonitor()
monitor.login()

monitor_thread=monitor.start_monitoring() 

@app.route('/get_ranking', methods=['GET'])
def get_ranking():
    with open('data.txt', 'r') as file:
        lines = file.readlines()
    # 从monitor对象获取最新排名信息
    latest_ranking=[]
    for i in range(-1, -10, -1):
        [formatted_time, current_user_name, current_problem_name] = eval(lines[i])
        latest_ranking.append(f"{formatted_time}:{current_user_name}: {current_problem_name}")  # 将排名数据添加到列表中
    return jsonify(latest_ranking)

@app.route('/', methods=['GET', 'POST'])
def index():
    global email, user_to_track
    if request.method == 'POST':
        # 获取表单数据
        email = request.form['email']
        user_to_track = request.form['user_to_track']
        # 您可以在这里执行相应的操作,例如更新配置文件或重新初始化monitor对象
        # monitor.aimed_user=user_to_track
        # monitor.receiver_email_address=email
        monitor.change_aim(user_to_track,email)
        
    return render_template('index.html', email=email, user_to_track=user_to_track)
    
if __name__ == '__main__':
    app.run("10.171.149.10",port=516,debug=True)
    monitor_thread.join()