from flask import Flask,request,jsonify,abort,Blueprint
import pymongo
from pymongo import MongoClient
import base64
import random
from db import db

auth_api = Blueprint('auth',__name__,url_prefix='/')
auth_db=db['auth']




@auth_api.route('/register',methods=['POST'])
def regiser():
    
    user_id=request.args.get('id')
    pw=request.args.get('pw')
    email=request.args.get('email')
    name=request.args.get('name')
    
    if user_id==None or pw==None or email==None or name==None:
        return jsonify(message='매개변수가 비어있습니다',code=400)
   
    for i in auth_db.find({'id':user_id}):
        return jsonify(message='이미 있는 아이디 입니다',code= 403)   

    

    auth_db.insert({'email':email, "name":name,"id": user_id,"pw":base64.b64encode(pw.encode('euc-kr'))})
    return jsonify(message="success",code=200)

    
@auth_api.route('/auth',methods=['POST'])
def login():
    data=request.data.decode('utf-8')
    
    
    user_id=request.args.get('id')
    pw=request.args.get('pw')
    a=auth_db.find({'id':user_id})
    for i in a:
        print(i)
        if i['pw']==base64.b64encode(pw.encode('euc-kr')):
            
            jsons={'name':i['name']}
            return jsonify(code=200,message="seccess",data=jsons)
        else:
            return jsonify(code=403,message='login fail')

    if user_id==None or pw==None:
        return jsonify(message="Id or Pw was Null",code=403)
    return jsonify(message="don't this id ow pw",code=403)
