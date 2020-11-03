from flask import Flask,request,jsonify,abort,Blueprint
import base64
from db import db
import jwt
from datetime import datetime, timedelta
from Decorator import login_required

auth_api = Blueprint('auth',__name__,url_prefix='/')
auth_db=db['auth']
auth_api.config = {}
auth_api.config['JWT_SECRET_KEY']='alswns0221'

@auth_api.route('/user',methods=['GET'])
@login_required
def get_id(data):
    print('아이디는?!?!?')
    print('\n'+data)
    user_id=data.get('id')
    print(data['id'])
    if user_id!=None:
        return jsonfy(code=200,id=user_id,data=data)
    else:
        return jsonfy(code=400)

@auth_api.route('/register',methods=['POST'])
def regiser():
    data=request.get_json()
    
    user_id=data.get('id')
    pw=data.get('pw')
    email=data.get('email')
    name=data.get('name')
    
    # request.data
    if user_id==None or pw==None or email==None or name==None:
        return jsonify(message='매개변수가 비어있습니다',code=400)
   
    for i in auth_db.find({'id':user_id}):
        return jsonify(message='이미 있는 아이디 입니다',code= 403)   

    auth_db.insert({'email':email, "name":name,"id": user_id,"pw":base64.b64encode(pw.encode('euc-kr'))})
    return jsonify(message="success",code=200)

    
@auth_api.route('/auth',methods=['POST'])
def login():

    data=request.get_json()

    user_id=data.get('id')
    pw=data.get('pw')

    a=auth_db.find({'id':user_id})
    for i in a:
        print(i)
        if i['pw']==base64.b64encode(pw.encode('euc-kr')):
            payload={
                'user_id':user_id,
                'exp':datetime.utcnow() + timedelta(seconds = 60 * 60 * 24),
            }
            #
            token=jwt.encode(payload,auth_api.config['JWT_SECRET_KEY'],'HS256')

            return jsonify(code=200,message="seccess",access_token=token.decode('UTF-8'))
        else:
            return jsonify(code=403,message='login fail')

    if user_id==None or pw==None:
        return jsonify(message="Id or Pw was Null",code=403)
    return jsonify(message="don't this id ow pw",code=403)
