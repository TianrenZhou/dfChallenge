import pymongo
from pymongo import MongoClient
import flask
from flask import current_app as app, request
from flask import jsonify

ERROR = "Name of NOTE/TODO required"
INVALID_BODY = "Invalid body"
NOT_FOUND = "No such TODO/NOTE found"
EXIST = "TODO/NOTE already exists"

client = MongoClient()
db = client.notes
app = flask.Flask(__name__)
app.config['DEBUG'] = True

#default
@app.route('/',methods=['GET'])
def home():
    return "Challenge"

#Create new note
@app.route('/create',methods=['PUT'])
def create():
    if 'name' in request.args:
        noteName = request.args['name']
    else:
        return {"status":400,"message":ERROR}
    collists = db.list_collection_names()
    if noteName in collists:
        return {"status":200,"message":EXIST}
    col = db[noteName]
    col.insert_one({"TODO":"default"})
    return {"status":200,"message":"NOTE created!"}

#add TODOs
@app.route('/add',methods=['PUT'])
def add():
    body = request.json
    if not body:
        return {"status":400,"message":INVALID_BODY}
    if 'name' in request.args:
        noteName = request.args['name']
    else:
        return {"status":400,"message":ERROR}
    col = db[noteName]
    col.insert_one(body)
    return {"status":200,"message":"TODOs added!"}

#complete TODOs
@app.route('/complete',methods=['delete'])
def complete():
    body = request.json
    if not body:
        return {"status":400,"message":INVALID_BODY}
    if 'name' in request.args:
        noteName = request.args['name']
    else:
        return {"status":400,"message":ERROR}
    col = db[noteName]
    res = col.delete_one(body)
    if res == None:
        return {"status":404,"message":NOT_FOUND}
    return {"status":200,"message":"TODO completed!"}

#list all TODOs
@app.route('/list',methods=['GET'])
def lst():
    if 'name' in request.args:
        noteName = request.args['name']
    else:
        return {"status":400,"message":ERROR}
    collists = db.list_collection_names()
    if not noteName in collists:
        return {"status":404,"message":NOT_FOUND}
    col = db[noteName]
    res = col.find({"TODO":{"$ne":"default"}},{"_id":0})
    json_doc = []
    for doc in res:
        json_doc.append(doc)
    return jsonify(json_doc)

#delete TODOs
@app.route('/delete_TODO',methods=['delete'])
def delete_TODO():
    body = request.json
    if not body:
        return {"status":400,"message":INVALID_BODY}
    if 'name' in request.args:
        noteName = request.args['name']
    else:
        return {"status":400,"message":ERROR}
    col = db[noteName]
    res = col.delete_one(body)
    if res == None:
        return {"status":404,"message":NOT_FOUND}
    return {"status":200,"message":"TODO deleted!"}

#delete NOTEs
@app.route('/delete_NOTE',methods=['delete'])
def delete_NOTE():
    if 'name' in request.args:
        noteName = request.args['name']
    else:
        return {"status":400,"message":ERROR}
    collists = db.list_collection_names()
    if not noteName in collists:
        return {"status":404,"message":NOT_FOUND}
    col = db[noteName]
    col.drop()
    return {"status":200,"message":"NOTE deleted!"}
app.run()