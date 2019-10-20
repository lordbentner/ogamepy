from flask import Flask
import ogamebot

app = Flask(__name__)


@app.route('/')
def hello():
    return ogamebot.global_launch()

if __name__ == '__main__':
    app.run()