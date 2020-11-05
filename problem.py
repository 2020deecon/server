from flask import Flask,request,jsonify,abort,Blueprint
import flask
import pymongo
from pymongo import MongoClient
import base64
import random
from db import db
from Decorator import login_required

problem_api = Blueprint('problem',__name__,url_prefix='/')
problem_db=db['problem']

@problem_api.route('/problem',methods=['POST'])
@login_required
def problem(user):
    print(user.get('email'))
    try:
        # image=request.files['image']
        data=request.get_json()
        print(data)
        if data==None:
            data={}
        title=data.get('title')
        problem_type=data.get('type')
        answer=data.get('answer')
        category=data.get('category')
        
        sub_title=data.get('sub_title')
        image=data.get('image')

    except Exception as e:
        return jsonify(error=str(e),message='server error',code=400)
    
    if title==None or problem_type==None or answer==None or category==None:
        return jsonify(message='매개변수가 비어있습니다',code=400)
    problem_db.insert({'id':user.get('id'),'title':title, "sub_title":sub_title,"image": image,"answer":answer,'category':category})
    
    return jsonify(message='success',code=200)

@problem_api.route('/sendProblem',methods=['GET'])
def send_problem():
    problem_list=[]
    problems=problem_db.find({})
    print(problems)
    for problem in problems:
        problem_list.append(problem)

    return jsonify(code=200,data=problem_list)
        
        
    
a