from flask import Flask ,jsonify
from flask import render_template
from ogamebot import Afficheur
import os

HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'flask')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
HOME_DIR = os.environ.get('OPENSHIFT_HOMEDIR', os.getcwd())

"""dir_path = os.path.dirname(os.path.realpath(__file__))
IP
if("opt" in dir_path):"""

app = Flask(__name__)
thread_1 = Afficheur()

def launch_ogame():
    global thread_1
    thread_1.daemon = True
    thread_1.start()

@app.route('/')
def hello():
    return render_template('index.html',ogame=thread_1.ogame_infos,
    len=len(thread_1.ogame_infos),research=thread_1.lvl_research,isCon=thread_1.isConnected)

@app.route('/refresh/', methods=['POST'])
def refresh():
    return render_template('index.html',ogame=thread_1.ogame_infos,
    len=len(thread_1.ogame_infos),research=thread_1.lvl_research,isCon=thread_1.isConnected)

@app.route("/start/", methods=['POST'])
def start():
    thread_1.isRunning = True
    return render_template('index.html')

@app.route("/stop/", methods=['POST'])
def stop():
    thread_1.StopRunning()
    return render_template('index.html')

if __name__ == '__main__':
    launch_ogame()
    app.run(use_reloader = True,host=IP,port=PORT)

#use_reloader = True,
#host='0.0.0.0', port=PORT