from flask import Flask
from flask import request
from flask import json


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return("Hello webhooks")

@app.route('/pull_req', methods=['POST'])
def gh_pull():
    pass


if __name__ == '__main__':
    app.run(debug=True)



