from flask import request,jsonify,abort,Blueprint
from .db import db
from .Decorator import login_required
from bson.objectid import ObjectId
from datetime import datetime

comunity_api = Blueprint('comunity',__name__,url_prefix='/')
comunity_db=db['comunity']
comment_db=db['comment']

def getDateTime() -> int:

    dt_obj = datetime.strptime('20.12.2016 09:38:42,76',
                            '%d.%m.%Y %H:%M:%S,%f')
    millisec = dt_obj.timestamp() * 1000


    return int(millisec)

@comunity_api.route('/makePost',methods=['POST'])
@login_required
def makePost(data):
    if data==None:
        return jsonify(code=400,message='check token')

    user_id=data.get('id')
    data=request.get_json()
    
    title=data.get('title')
    image=data.get('image')
    text=data.get('text')
    post_type=data.get('type')
    if title==None   or text==None:
        return jsonify(code=400,message='매개변수가 비었습니다')
    comunity_db.insert({'type':post_type,'write_id':user_id,'time':getDateTime(),'title':title,'image':image,'text':text})
    return jsonify(code=200,message='성공')

@comunity_api.route('/sendPost',methods=['GET'])
def sendPost():
    data=comunity_db.find().sort('time',1)
    post_list=[]
    for i in data:
        post_dict=dict()
        post_dict['id']=str(i.get('_id'))
        post_dict['title']=i.get('title')
        post_dict['text']=i.get('text')
        post_dict['time']=i.get('time')
        post_dict['type']=i.get('type')
        post_dict['image']=i.get('image')
        post_list.append(post_dict)
    return jsonify(code=200,data=post_list)

@comunity_api.route('/sendComment',methods=['GET'])
def sendComment():
    data=request.args
    project_id=data.get('id')
    
    if project_id==None:
        return jsonify(code=403,messege='pls comment_id')
    comments=comment_db.find({'project_id':project_id})
    return jsonify(code=200,data=comments)

@comunity_api.route('/detailPost',methods=['GET'])
def detailPost():
    data=request.args
    comunity_id=data['id']
    objectId=ObjectId(comunity_id)
    post=None
    comment_list=[]
    for i in comunity_db.find({'_id':objectId}):
        post=i
    for i in comment_db.find({'project_id':comunity_id}).sort('time'):
        del i['_id']
        i['_id']=None
        comment_list.append(i)
    
    #del post['_id']
    #post['_id']=None
    post['_id']=str(post['_id'])
    post['comment']=comment_list
    return jsonify(code=200,data=post)
    



    post_list=[]
    for i in data:
        post_dict=dict()
        post_dict['id']=str(i.get('_id'))
        post_dict['title']=i.get('title')
        post_dict['text']=i.get('text')
        post_dict['time']=i.get('time')
        post_list.append(post_dict)
    return jsonify(code=200,data=post_dict)






@comunity_api.route('/makeComment',methods=['POST'])
@login_required
def makeComment(data):
    if data==None:
        return jsonify(code=400,message='check token')
    user_id=data.get('id')
    data=request.get_json()

    comment=data.get('comment')
    project_id=data.get('project_id')
    if user_id==None or comment ==None or project_id==None:
        return jsonify(code=400,message='매개변수가 비었습니다')            
    comment_db.insert({'comment':comment,'writer':user_id,'project_id':project_id,'time':getDateTime()})    
    return jsonify(code=200,message='성공!')

    

    
    
