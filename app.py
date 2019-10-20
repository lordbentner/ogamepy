from flask import Flask
from flask import render_template
from ogamebot import Afficheur

app = Flask(__name__)
thread_1 = Afficheur("1")


@app.route('/')
def hello():
    return render_template('index.html',ogame=thread_1.ogame_infos)

if __name__ == '__main__':
    thread_1.start()
    app.run()