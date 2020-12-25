from flask import Flask,request,jsonify,abort,Blueprint
# from .dialogflow import Dialogflow

from google.dialogflow import Dialogflow
chatbot_api = Blueprint('chatbot',__name__,url_prefix='/')
dialogflow=Dialogflow()

@chatbot_api.route('/chatbot',methods=['GET'])
def chat():
    data=request.args
    
    comment=data.get('comment')
    if comment==None:
        return jsonify(code=403,message="There is not comment")
    else:
        chat=dialogflow.predict(comment)
        if chat == None:
            return jsonify(code=403,message="error")
        return jsonify(code=200,chat=chat)



