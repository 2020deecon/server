from flask import request,jsonify,abort,Blueprint
from db import db
from Decorator import login_required
from bson.objectid import ObjectId
from datetime import datetime

comunity_api = Blueprint('comunity',__name__,url_prefix='/')
comunity_db=db['comunity']
comment_db=db['comment']

def getDateTime() -> int:

    dt_obj = datetime.strptime('20.12.2016 09:38:42,76',
                            '%d.%m.%Y %H:%M:%S,%f')
    millisec = dt_obj.timestamp() * 1000

    print(int(millisec))

    return int(millisec)

@comunity_api.route('/makePost',methods=['POST'])
@login_required
def makePost(data):
    user_name=data.get('name')
    data=request.get_json()
    
    title=data.get('title')
    image=data.get('image')
    text=data.get('text')

    if title==None or image==None or text==None:
        return jsonify(code=400,message='매개변수가 비었습니다')
    comunity_db.insert({'write_id':user_id,'time':getDateTime(),'title':title,'image':image,'text':text})

@comunity_api.route('/sendPost',methods=['GET'])
def sendPost():
    data=comunity_db.find({})
    post_list=[]
    for i in data:
        post_dict=dict()
        post_dict['id']=str(i['_id'])
        post_dict['title']=i['title']
        post_dict['text']=i['text']
        post_dict['time']=i['time']
        post_list.append(post_dict)
    return jsonify(code=200,data=post_dict)

@comunity_api.route('/detailPost',methods=['GET'])
def detailPost():
    data=request.args
    comunity_id=data['id']
    objectId=ObjectId(comunity_id)
    post=None
    comment_list=[]
    for i in comunity_db.find({'_id':objectId}):
        post=i
    for i in comunity_db.find({'project_id':comunity_id}):
        del i['_id']
        comment_list.append(i)
    
        del post['_id']
        post['comment']=comment_list
        
    return jsonify(code=200,data=post)
    



    post_list=[]
    for i in data:
        post_dict=dict()
        post_dict['id']=str(i['_id'])
        post_dict['title']=i['title']
        post_dict['text']=i['text']
        post_dict['time']=i['time']
        post_list.append(post_dict)
    return jsonify(code=200,data=post_dict)






@comunity_api.route('/makeComment',methods=['POST'])
@login_required
def makeComment(data):
    user_name=data.get('name')
    data=request.get_json()

    comment=data.get('comment')
    project_id=data.get('project_id')

    if user_name==None or comment ==None or project_id==None:
        return jsonify(code=400,message='매개변수가 비었습니다')            
    comunity_db({'comment':comment,'writer':user_name,'project_id':project_id,'time':getDateTime()})    

    

    
    