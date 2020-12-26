from google.oauth2 import service_account
import google.auth.transport.requests as re
import requests
import json
import google.oauth2 as google

class Dialogflow:
    def __init__(self):        
        client_secret ='google/dialogflow.json'
        scope=['https://www.googleapis.com/auth/dialogflow']
        

        self.creds = service_account.Credentials.from_service_account_file(
                client_secret)
        self.creds=self.creds.with_scopes(scope)
        
        self.refresh_token()

        self.url = 'https://dialogflow.googleapis.com/v2/projects/deecon-axjo/agent/sessions/123456:detectIntent'
        self.headers=dict()
        self.data=dict()
        
    def refresh_token(self):
        http=re.Request()
        self.creds.refresh(http)

    def predict(self,string):
        if self.creds.valid:
            self.refresh_token()

        self.make_data(string)
        res=requests.post(self.url,data=self.data,headers=self.headers)
        
        if res.status_code==200:
            chat = res.json().get('queryResult').get('fulfillmentText')
            return chat
        else:
            return None

    def make_data(self,string):
        comment=string
        self.headers={
                    'Content-Type': 'application/json; charset=utf-8',
                    'Authorization':  'Bearer '+self.creds.token 
                }

        self.data = {
                "queryInput": {
                    "text": {
                        "text": comment,
                        "language_code": "en-US"
                    }
                }
            }
        self.data=json.dumps(self.data)

if __name__ == "__main__":
    dialogflow=Dialogflow()
    dialogflow.predict('안녕')
    dialogflow.predict('안녕')
    dialogflow.predict('안녕')