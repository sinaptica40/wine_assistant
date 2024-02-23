from src.app import createApp
import os
from dotenv import load_dotenv, find_dotenv
from flask import render_template

load_dotenv(find_dotenv())

port = os.getenv('FLASK_PORT')
host = os.getenv('FLASK_HOST')
env_name = os.getenv('FLASK_ENV')

if env_name == "development":
    debug = True
else:
    debug = False

app = createApp()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # run app
    app.run(debug=debug, host=host, port=port)
    #socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
