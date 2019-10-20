from flask import Flask
from flask import render_template
import ogamebot

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html',ogame=ogamebot.ogame_infos)

if __name__ == '__main__':
    app.run()