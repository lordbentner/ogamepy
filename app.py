from flask import Flask ,jsonify
from flask import render_template
from ogamebot import Afficheur
import os

HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'flask')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
HOME_DIR = os.environ.get('OPENSHIFT_HOMEDIR', os.getcwd())

app = Flask(__name__)
thread_1 = Afficheur()

def launch_ogame():
    try:
        thread_1 = Afficheur()
        thread_1.daemon = True
        thread_1.start()
    except:
        launch_ogame()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/start/", methods=['POST'])
def start():
    thread_1 = Afficheur()
    thread_1.start()
    thread_1.join()
    return render_template('index.html', ogame=thread_1.ogame_infos)

@app.route('/refresh/', methods=['POST'])
def refresh():
    return render_template('index.html', ogame=thread_1.ogame_infos)

@app.route("/stop/", methods=['POST'])
def stop():
    thread_1.join()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)