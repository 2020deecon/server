from flask import Flask
import flask
from auth import auth_api
from problem import problem_api
import logging

app = Flask(__name__)
# app.logger.setLevel(logging.ERROR)
app.register_blueprint(auth_api)
app.register_blueprint(problem_api)



@app.route('/', methods=["GET", "DELETE", "OPTIONS"])
def index():
    my_res = flask.Response()
 
    http_method = flask.request.method
 
    if http_method == "OPTIONS": # 사전요청
        print("--사전 요청(Preflight Request)--")
        my_res.headers.add("Access-Control-Allow-Origin", "*")
        my_res.headers.add('Access-Control-Allow-Headers', "*")
        my_res.headers.add('Access-Control-Allow-Methods', "GET,DELETE")
    elif http_method == "GET": # 실제요청
        print("--실제 요청--")
        my_res.headers.add("Access-Control-Allow-Origin", "*")
        my_res.set_data("deecon server")
    elif http_method == "DELETE": # 실제요청
        print("--실제 요청--")
        my_res.headers.add("Access-Control-Allow-Origin", "*")
        my_res.set_data("삭제했지롱")
    else: 
        print("요구하지 않은 HTTP METHOD(" + http_method + ")입니다.")       
    
    return my_res



if __name__=='__main__':
    # app.run(host='0.0.0.0',port=3000) 
    app.run(host='0.0.0.0',port=3000, debug=True) 

