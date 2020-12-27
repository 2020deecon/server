import jwt
from functools  import wraps
from flask 		import request, Response ,jsonify
from .db import db
auth=db['auth']
config='alswns0221'
def login_required(f):     
    user_info=[] 
    def get_user(user_id):
        x = auth.find_one({'id':user_id})
        return x
    									
    @wraps(f)                   								
    def decorated_function(*args, **kwargs):
        user_info=[]
        payload='init'					
        access_token = request.headers.get('Authorization') 	
        if access_token is not None:  							
            try:    
                payload = jwt.decode(access_token, config, algorithms=['HS256'])			   
            except jwt.InvalidTokenError as e:
                payload = None   

            if payload is None: return jsonify(messege='need Authorization',status=401)  	
            
            user_id   = payload['user_id']  					
            # user_id = user_id
            user    = get_user(user_id) if user_id else None
        else:
            return jsonify(messege='There is not Access Token',status=401)  	

        return f(user,*args, **kwargs)
    return decorated_function
