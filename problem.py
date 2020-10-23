from flask import Flask,request,jsonify,abort,Blueprint
import flask
import pymongo
from pymongo import MongoClient
import base64
import random
from db import db

problem_api = Blueprint('problem',__name__,url_prefix='/')
problem_db=db['problem']

@problem_api.route('/problem')
def problem():
    try:
        title=request.args.get('title')
        sub_title=request.args.get('sub_title')
        image=request.args.get('image')
        # image=request.files['image']
        answer=request.args.get('answer')
        category=request.args.get('category')
    except Exception as e:
        print(type(image))
        return jsonify(error=str(e),message='server error',code=400)
    print(image)
    
    if title==None or sub_title==None or sub_title==None or answer==None or category==None:
        return jsonify(message='매개변수가 비어있습니다',code=400)
    problem_db.insert({'title':title, "sub_title":sub_title,"image": image,"answer":answer,'category':category})
    
    return jsonify(message='success',code=200)
