from flask import Flask
from flask import render_template
from ogamebot import Afficheur

app = Flask(__name__)


@app.route('/')
def hello():
    thread_1 = Afficheur("1")
    thread_1.start()
    return render_template('index.html',ogame=Afficheur.ogame_infos)

if __name__ == '__main__':
    app.run()