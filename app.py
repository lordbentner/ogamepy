from flask import Flask
from flask import render_template
from ogamebot import Afficheur

app = Flask(__name__)
thread_1 = Afficheur("1")

def launch_ogame():
    try:
        thread_1 = Afficheur("1")
        thread_1.start()
    except:
        launch_ogame()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/start/", methods=['POST'])
def start():
    launch_ogame()
    return render_template('index.html', ogame=thread_1.ogame_infos)

@app.route('/refresh/')
def refresh():
    return render_template('index.html', ogame=thread_1.ogame_infos)

@app.route("/stop/", methods=['POST'])
def stop():
    thread_1.StopRunning()
    thread_1.join()
    return render_template('index.html')

if __name__ == '__main__':
    app.run()