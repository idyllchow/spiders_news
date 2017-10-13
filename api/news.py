import os
from pymongo import MongoClient
from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)
print('app path: %s' % app)
mongo = PyMongo(app)

db_name = 'news_items'
table_name = 'news_content'


def __init__(self, mongo_uri, mongo_db):
    self.mongo_uri = mongo_uri
    self.mongo_db = mongo_db

MONGODB_URI = os.environ.get('MONGODB_URI')
if not MONGODB_URI:
    print('mongo uri has\'t been found')
    db = MongoClient('localhost', 27017)[db_name]
else:
    print('mongo uri has been found %s: ' % MongoClient(MONGODB_URI)[db_name])
    db = MongoClient(MONGODB_URI)[db_name]


def to_json(data):
    return json.dumps(data, default=json_util.default)


@app.route('/news/title', methods=['GET'])
def get_news_title():
    if request.method == 'GET':
        results = db[table_name].find({}, {'title': 1})
        json_results = ''
        for result in results:
            result.pop('_id')
            json_results.append(result)
        return to_json(json_results)


@app.route('/news', methods=['GET'])
def get_limit_news():
    if request.method == 'GET':
        index = request.args.get('index')
        count = request.args.get('count')
        if index is '':
            results = db[table_name].find().limit(count)
        else:
            results = db[table_name].find({"index": {"$gt": index}, "index": {"$lte": index + count}})
        total_num = db[table_name].find().count()
        json_results = []
        print('======result=====%s' % db)
        for result in results:
            result.pop('_id')
            json_results.append(result)
        # return to_json(json_results)
        return jsonify({"total_num": total_num, "news": json_results})


@app.route('/news', methods=['GET'])
def get_all_news():
    if request.method == 'GET':
        results = db[table_name].find()
        json_results = []
        for result in results:
            print('======result before=====%s' % result)
            result.pop('_id')
            print('======result=====%s' % result)
            json_results.append(result)
        return to_json(json_results)


@app.route('/news/single_news/title', methods=['GET'])
def get_single_news_by_title():
    if request.method == 'GET':
        title = request.args.get('title')
        result = db[table_name].find({'title': title})
        result.pop('_id')
        return str(json_util.dumps(result))


@app.route('/news/single_news/id', methods=['GET'])
def get_single_news():
    if request.method == 'GET':
        object_id = ObjectId(request.args.get('id'))
        result = db[table_name].find({'_id': object_id})
        # cover_result = json_util.dumps(result)
        # import pdb; pdb.set_trace()
        result.pop('_id')
        return json_util.dumps(result)


if __name__ == '__main__':
    app.run()
