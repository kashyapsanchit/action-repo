from flask import Flask, render_template
from flask import request
import datetime
from flask import json
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads

app = Flask(__name__, template_folder= 'template')
app.config["MONGO_URI"] = "mongodb+srv://sanchit:sanchit@cluster0.sqntw.gcp.mongodb.net/action?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def index():
    return("Webhooks")

@app.route('/github', methods=['GET' ,'POST'])
def gh_webhooks():
    if request.headers["Content-Type"] == 'application/json':
        
        if request.json['action']:
            data = dict(
                request_id = request.json['pull_request']['id'],
                author = request.json["sender"]['login'],
                action = "PULL_REQUEST",
                from_branch = request.json['pull_request']["head"]["ref"],
                to_branch = request.json['pull_request']['base']['ref'],
                created_at = request.json['pull_request']['created_at'],
                updated_at = request.json['pull_request']['updated_at']
            )
            db.reqs.insert_one(data)

            cur = db.reqs.find()
            data = dumps(list(cur))
            d = loads(data)
            print(d[-1])
            author = d[-1]['author']
            action = d[-1]['action']
            from_branch = d[-1]['from_branch']
            to_branch = d[-1]['to_branch']
            created_at = d[-1]['created_at']

            return render_template('index.html', author = author, action=action, from_branch=from_branch, to_branch=to_branch, created_at= created_at )
            
        elif request.json['ref']:

            data = dict(
            request_id = request.json['commits'][0]['id'],
            author = request.json["pusher"]['name'],
            action = "PUSH",
            to_branch= str(request.json["ref"]).split('/')[2],
            timestamp = request.json['commits'][0]['timestamp']
            )   

            db.reqs.insert_one(data)

            cur = db.reqs.find()
            data = dumps(list(cur))
            d = loads(data)
            print(d[-1])
            author = d[-1]['author']
            action = d[-1]['action']
            to_branch = d[-1]['to_branch']
            timestamp = d[-1]['timestamp']
    
            return render_template('index.html', author = author, action=action, to_branch=to_branch, timestamp= timestamp )

        
    return("Success")

        
#         return render_template('index.html', author = author, action=action, from_branch=from_branch, to_branch=to_branch, created_at= created_at )
#     return("Success")


# @app.route('/push_req', methods=['POST'])
# def gh_push():
#     if request.headers["Content-Type"] == 'application/json':
        
        
#     if request.method == "GET":

#     return("Push Request")



if __name__ == '__main__':
    app.run(debug=True)



