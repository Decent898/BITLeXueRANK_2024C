# app.py
from flask import Flask, render_template, request
from flask import jsonify
from main import OnlineCompetitionMonitor

app = Flask(__name__)

email = ""
user_to_track = ""

monitor = OnlineCompetitionMonitor()
monitor.login()

monitor_thread=monitor.start_monitoring() 

@app.route('/get_ranking', methods=['GET'])
def get_ranking():
    with open('data.txt', 'r') as file:
        lines = file.readlines()
    latest_ranking=[]
    for i in range(-1, -10, -1):
        [formatted_time, current_user_name, current_problem_name] = eval(lines[i])
        latest_ranking.append(f"{formatted_time}: {current_user_name}: {current_problem_name}")  # 将排名数据添加到列表中
    return jsonify(latest_ranking)

@app.route('/', methods=['GET', 'POST'])
def index():
    global email, user_to_track
    if request.method == 'POST':
        email = request.form['email']
        user_to_track = request.form['user_to_track']
        monitor.change_aim(user_to_track,email)
        
    return render_template('index.html', email=email, user_to_track=user_to_track)
    
if __name__ == '__main__':
    app.run("10.171.149.10",port=516,debug=False)
    monitor_thread.join()