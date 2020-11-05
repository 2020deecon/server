from flask import Flask
import flask
from auth import auth_api
from problem import problem_api
from flask_cors import  CORS, cross_origin
from community import comunity_api

app = Flask(__name__)
# app.logger.setLevel(logging.ERROR)
app.register_blueprint(auth_api)
app.register_blueprint(problem_api)
app.register_blueprint(comunity_api)

CORS(app)

@app.route('/', methods=["GET", "DELETE", "OPTIONS"])
def index():
         
    
    return 'deecon server'



if __name__=='__main__':
    # app.run(host='0.0.0.0',port=3000) 
    app.run(host='0.0.0.0',port=3000, debug=True) 

