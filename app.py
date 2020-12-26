from flask import Flask
import flask
from flask_cors import  CORS, cross_origin

# from auth import auth_api
# from problem import problem_api
# from community import comunity_api
# from chatbot import chatbot_api
from BluePrint import auth,chatbot,community,problem
app = Flask(__name__)
# app.logger.setLevel(logging.ERROR)

app.register_blueprint(auth.auth_api)
app.register_blueprint(problem.problem_api)
app.register_blueprint(community.comunity_api)
app.register_blueprint(chatbot.chatbot_api)

CORS(app)

@app.route('/', methods=["GET", "DELETE", "OPTIONS"])
def index():
    return 'deecon server'

if __name__=='__main__':
    #app.run(host='0.0.0.0',port=3000) 
    app.run(host='0.0.0.0',port=3000, debug=True) 

