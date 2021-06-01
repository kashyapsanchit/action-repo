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
        
        req_action = request.json['action']
        if request.json['action'] == 'opened':
            req_action = "PULL_REQUEST"
        elif request.json['action'] == 'closed':
            req_action = "MERGE"
        
        data = dict(
            request_id = request.json['pull_request']['id'],
            author = request.json["sender"]['login'],
            action = req_action,
            from_branch = request.json['pull_request']["head"]["ref"],
            to_branch = request.json['pull_request']['base']['ref'],
            created_at = request.json['pull_request']['created_at'],
            updated_at = request.json['pull_request']['updated_at']
        )

        db.reqs.insert_one(data)
        return("Success")

    author = db.reqs["author"]
    from_branch = db.reqs["from_branch"]
    to_branch = db.reqs["to_branch"]
    print(author)
    return("Data added")


@app.route('/push_req', methods=['POST'])
def gh_push():
    if request.headers["Content-Type"] == 'application/json':
        
        data = dict(
            request_id = request.json['commits'][0]['id'],
            author = request.json["pusher"]['name'],
            action = "PUSH",
            timestamp = request.json['commits'][0]['timestamp']
        )

        db.reqs.insert_one(data)

            
        return("Success")

    
    return("Push Request")




if __name__ == '__main__':
    app.run(debug=True)



