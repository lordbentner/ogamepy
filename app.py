from flask import Flask ,jsonify,render_template,request
from ogamebot import Afficheur
from ogame.constants import Missions
import os, sys
from multiprocessing import Process

HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'flask')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
HOME_DIR = os.environ.get('OPENSHIFT_HOMEDIR', os.getcwd())

dir_path = os.path.dirname(os.path.realpath(__file__))

if("opt" in dir_path):
    IP='0.0.0.0'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
thread_1 = Afficheur()

def launch_ogame():
    global thread_1
    thread_1.daemon = True
    thread_1.start()

@app.route('/')
def hello():
    info = [ thread_1.isConnected,thread_1.isRunning,
     thread_1.f_o.inResearch.items(),thread_1.co_gal,thread_1.co_sys, thread_1.i_o.nbmessage]
    return render_template('index.html',ogame=thread_1.ogame_infos,
    research=thread_1.lvl_research,info=info)

@app.route('/refresh/')
def refresh():
    info = [ thread_1.isConnected,thread_1.isRunning, thread_1.f_o.inResearch.items()]
    return render_template('index.html',ogame=thread_1.ogame_infos,
    research=thread_1.lvl_research,info=info)

@app.route("/start/")
def start():
    thread_1.StartRunning()
    return refresh()

@app.route("/stop/")
def stop():
    thread_1.StopRunning()
    return refresh()

@app.route("/log/")
def log():
    return render_template('log.html',info_log=thread_1.info_log,info_log2=thread_1.infoLog2)

@app.route("/flottes/")
def flottes():
    return render_template('flottes.html',flottes=thread_1.fleets ,missions_list=Missions.items())

def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

@app.route("/quit/")
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return refresh()

if __name__ == '__main__':
    launch_ogame()
    app.run(use_reloader = True,host=IP,port=PORT,debug=True)