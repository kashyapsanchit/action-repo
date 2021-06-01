from flask import Flask
from flask import request
import datetime
from flask import json
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sanchit:sanchit@cluster0.sqntw.gcp.mongodb.net/action?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def index():
    return("Hahahah")

@app.route('/pull_req', methods=['POST'])
def gh_pull():
    if request.headers["Content-Type"] == 'application/json':
        print(request.json)

        # if request.json['action'] == 'opened':
        #     req_action = "PULL_REQUEST"
        
        data = dict(
            request_id = request.json['pull_request']['id'],
            author = request.json["sender"]['login'],
            action = request.json['action'],
            from_branch = request.json['pull_request']["head"]["ref"],
            to_branch = request.json['pull_request']['base']['ref'],
            created_at = request.json['pull_request']['created_at'],
            updated_at = request.json['pull_request']['updated_at']
        )

        db.reqs.insert_one(data)
        return("Success")
    
    return("Data added")


# @app.route('/push_req', methods=['POST'])
# def gh_push():
#     if request.headers["Content-Type"] == 'application/json':




if __name__ == '__main__':
    app.run(debug=True)



