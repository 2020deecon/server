from flask import Flask,request,jsonify,abort,Blueprint
import flask
import pymongo
from pymongo import MongoClient
import base64
import random
from .db import db
from .Decorator import login_required
from bson.objectid import ObjectId

problem_api = Blueprint('problem',__name__,url_prefix='/')
problem_db=db['problem']
workbook_db=db['workbook']
wrong_anser_note_db=db['wrong_anser_note_db']

@problem_api.route('/problem',methods=['POST'])
@login_required
def problem(user):
    if user==None:
        return jsonify(code=400,message='check token')
    try:
        # image=request.files['image']
        data=request.get_json()
        if data==None:
            data={}
        title=data.get('title')
        problem_type=data.get('type')
        answer=data.get('answer')
        view=data.get('view')
        category=data.get('category')
        
        sub_title=data.get('sub_title')
        image=data.get('image')


    except Exception as e:
        return jsonify(error=str(e),message='server error',code=400)
    
    if title==None or problem_type==None or answer==None or category==None:
        return jsonify(message='매개변수가 비어있습니다',code=400)
    if problem_type =='true' and view==None:
        return jsonify(message='매개변수가 비어있습니다',code=400)  
    problem_db.insert({'id':user.get('id'),'problem_type':problem_type,'view':view,'title':title, "sub_title":sub_title,"image": image,"answer":answer,'category':category})
    
    return jsonify(message='success',code=200)

@problem_api.route('/sendProblem',methods=['GET'])
def send_problem():
    problem_list=[]
    problems=problem_db.find({})
    for problem in problems:
        data=dict()

        problem=dict(problem)
        object_id=problem.get('_id')
        object_id=str(object_id)
        problem['_id']=object_id
        
        data['category']=problem.get('category').encode('euc-kr').decode('euc-kr')
        data['_id']=object_id
        data['image']=problem.get('image')
        data['title']=problem.get('title')
        data['write_id']=problem.get('id')
        problem_list.append(data)
        
    return jsonify(code=200,data=problem_list )

#detailProblem query : id:id 
@problem_api.route('/detailProblem',methods=['GET'])
def detail_problem():
    data=request.args
    _id=data.get('id')
    objectId=ObjectId(_id)
    res=problem_db.find({'_id':objectId})
    data={}
    for i in res:
        data=i
        data['_id']=_id
    if data=={}:
        return jsonify(code=404,message="can not find this id")    
        
    return jsonify(code=200,data=data)
@problem_api.route('/myProblem',methods=['GET'])
@login_required
def myProblem(data):
    if data==None:
        return jsonify(code=400,message='check token')
    user_id=data.get('id')
    problems=problem_db.find({'id':user_id})
    problem_list=[]
    for problem in problems:
        req_dict=dict()
        req_dict['id']=str(problem['_id'])
        req_dict['title']=problem['title']
        req_dict['image']=problem['image']
        problem_list.append(req_dict)

    return jsonify(code=200,data=problem_list)
        
@problem_api.route('/workbookProblem',methods=['POST'])
@login_required
def workbookProblem(user):
    if user==None:
        return jsonify(code=400,message='check token')
    data=request.get_json()
    user_id=user.get('id')

    title=data.get('title')
    category=data.get('category')
    problem_id=data.get('problem_id')
    if title==None or category==None or problem_id==None:
        return jsonify(code=400,message='매개변수가 비어있습니다')
    
    workbook_db.insert({'title':title,'user_id':user_id,'category':category,'problem_id':problem_id})
    return jsonify(code=200,message='성공')

# @problem_api.route('/wrongNote',methods=['POST'])
# @login_required
# def wrongNote(user):
#     if user==None:
#         return jsonify(code=400,message='check token')
#     data=request.get_json()
#     user_id=user.get('id')

#     title=data.get('title')
#     #category=data.get('category')
#     problem_id=data.get('problem_id')
#     if title==None or  problem_id==None:
#         return jsonify(code=400,message='매개변수가 비어있습니다')
    
#     workbooks=wrong_anser_note_db.find({'user_id':user_id})
#     for i in workbooks:
#         return jsonify(code=403,message='이미 오답노트가 존재합니다')
#     wrong_anser_note_db.insert({'title':title,'user_id':user_id,'problem_id':problem_id})
#     return jsonify(code=200,message='성공')

@problem_api.route('/deleteWrongNote',methods=['POST'])
@login_required
def deleteWrongNote(user):
    if user==None:
        return jsonify(code=400,message='check token')
    user_id=user.get('id')
    wrong_anser_note_db.remove({'user_id':user_id})
    return jsonify(code=200,message='success')

@problem_api.route('/addWrongNote',methods=['POST'])
@login_required
def addWrongNote(user):
    if user==None:
        return jsonify(code=400,message='check token')
    user_id=user.get('id')

    workbooks=wrong_anser_note_db.find({'user_id':user_id})
    
    data=request.get_json()
    try:
        problems=data.get('problem')
        problem_list=[]
        for i in problems:
            problem_list.append(i.get('Id'))
            
        problems=problem_list
        
    except Exception as e:
        return jsonify(code=403,message='error',error_message=str(e))
    
    workbook_list=[]
    
    for workbook in workbooks:
        workbook_list=workbook['problem_id']
        workbook_list=list(set(workbook_list+problems))
        wrong_anser_note_db.update({'user_id':user_id},{'user_id':user_id,'problem_id':workbook_list})
        return jsonify(code=200,message='success')

    
    workbook_list=list(set(problems))
    wrong_anser_note_db.insert({'user_id':user_id,'problem_id':workbook_list})
    
    return jsonify(code=200,message='success')

@problem_api.route('/sendWrongNote',methods=['GET'])
@login_required
def sendWrongNote(user):
    if user==None:
        return jsonify(code=400,message='check token')
    user_id=user.get('id')
    workbooks=wrong_anser_note_db.find({'user_id':user_id})
    workbook_list=[]
    problem_id=[]
    for workbook in workbooks:
        problem_id=workbook['problem_id']
    for i in problem_id:
        
        problem=problem_db.find_one({'_id':ObjectId(i)})
        problem['id']=str( problem['_id'] )
        del problem['_id']
        workbook_list.append(problem)
    return jsonify(code=200,data=workbook_list)

@problem_api.route('/sendMineWorkbook',methods=['GET'])
@login_required
def sendMineWorkbook(user):
    if user==None:
        return jsonify(code=400,message='check token')
    user_id=user.get('id')
    workbooks=workbook_db.find({'user_id':user_id})
    workbook_list=[]
    for workbook in workbooks:
        workbook_dict={}
        workbook_dict['title']=workbook.get('title')
        workbook_dict['category']=workbook.get('category')
        workbook_dict['id']=str(workbook.get('_id'))
        workbook_list.append(workbook_dict)
    return jsonify(code=200,data=workbook_list)

@problem_api.route('/sendAllWorkbook',methods=['GET'])
def sendAllWorkbook():
    workbooks=workbook_db.find()
    workbook_list=[]
    for workbook in workbooks:
        workbook_dict={}
        workbook_dict['title']=workbook.get('title')
        workbook_dict['category']=workbook.get('category')
        workbook_dict['id']=str(workbook.get('_id'))
        workbook_dict['write_id']=workbook.get('user_id')
        workbook_list.append(workbook_dict)
    return jsonify(code=200,data=workbook_list)


@problem_api.route('/detailWorkbook',methods=['GET'])
def detailWorkbook():
    data=request.args
    workbook_id=data['id']
    objectId=ObjectId(workbook_id)

    workbooks=workbook_db.find({'_id':objectId})
    workbook=None
    for i in workbooks:
        workbook=i    
    if workbook==None:
        return jsonify(code=404,message='id에 일치하는 것이 없습니다')

    problem_id=workbook['problem_id']
    problem_list=[]
    for i in problem_id:
        objectId=ObjectId(i)
        res=problem_db.find({'_id':objectId})
        for j in res:
            j['_id']=str(j['_id'])
            problem_list.append(j)
    
    return jsonify(code=200,data={'problems':problem_list,'title':workbook['title']})
        


    