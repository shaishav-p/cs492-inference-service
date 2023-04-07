import logging
from flask import Flask, request
import constants
import torch
import torch.nn as nn
import copy

allFields_inputSize = 573
notProtectedFields_inputSize = 559
protectedFields_inputSize = 14

allFields_net = nn.Sequential(nn.Linear(allFields_inputSize, 2048),
                        nn.LeakyReLU(),
                        nn.Linear(2048, 1024),
                        nn.LeakyReLU(),
                        nn.Linear(1024, 512),
                        nn.LeakyReLU(),
                        nn.Linear(512, 256),
                        nn.LeakyReLU(),
                        nn.Linear(256, 128),
                        nn.LeakyReLU(),
                        nn.Linear(128, 64),
                        nn.LeakyReLU(),
                        nn.Linear(64,32),
                        nn.LeakyReLU(),
                        nn.Linear(32,1))

notProtectedFields_net = nn.Sequential(nn.Linear(notProtectedFields_inputSize, 2048),
                        nn.LeakyReLU(),
                        nn.Linear(2048, 1024),
                        nn.LeakyReLU(),
                        nn.Linear(1024, 512),
                        nn.LeakyReLU(),
                        nn.Linear(512, 256),
                        nn.LeakyReLU(),
                        nn.Linear(256, 128),
                        nn.LeakyReLU(),
                        nn.Linear(128, 64),
                        nn.LeakyReLU(),
                        nn.Linear(64,32),
                        nn.LeakyReLU(),
                        nn.Linear(32,1))

protectedFields_net = nn.Sequential(nn.Linear(protectedFields_inputSize, 2048),
                        nn.LeakyReLU(),
                        nn.Linear(2048, 1024),
                        nn.LeakyReLU(),
                        nn.Linear(1024, 512),
                        nn.LeakyReLU(),
                        nn.Linear(512, 256),
                        nn.LeakyReLU(),
                        nn.Linear(256, 128),
                        nn.LeakyReLU(),
                        nn.Linear(128, 64),
                        nn.LeakyReLU(),
                        nn.Linear(64,32),
                        nn.LeakyReLU(),
                        nn.Linear(32,1))


# allFields_net.load_state_dict(torch.load("allFields_net.pt",map_location=torch.device('cpu')))
allFields_net.load_state_dict(torch.load('allFields_net.pt', map_location=torch.device('cpu')))
notProtectedFields_net.load_state_dict(torch.load('notProtectedFields_net.pt', map_location=torch.device('cpu')))
protectedFields_net.load_state_dict(torch.load('protectedFields_net.pt', map_location=torch.device('cpu')))

allFields_net.eval()
notProtectedFields_net.eval()
protectedFields_net.eval()


# set logging level
logging.basicConfig(level=logging.INFO)
logging.info("(app.py) logging level set to INFO")

app = Flask(__name__)

@app.route("/")
def home():
   logging.info("received request for endpoint: / ")
   return "Hello, Flask!"


@app.route("/run-inference", methods=["GET", "POST"])
def run_inference():
   logging.info("received request for endpoint: /run-inference ")

   
   if request.method == "POST":
         # notProtectedFields_net.eval()
         # notProtectedFields_salary = nonProtectedFields_net()

         body = request.get_json()


         
         allFields = copy.deepcopy(constants.allFields)
         notProtectedFields = copy.deepcopy(constants.notProtectedFields)
         protectedFields = copy.deepcopy(constants.protectedFields)

         def updateKeysAndValues(inferenceModelKey, inferenceModelVal):
            
            if inferenceModelKey in allFields:
               allFields[inferenceModelKey] = inferenceModelVal

            if inferenceModelKey in notProtectedFields:
               notProtectedFields[inferenceModelKey] = inferenceModelVal

            if inferenceModelKey in protectedFields:
               protectedFields[inferenceModelKey] = inferenceModelVal
         
         for key in body:
            # get key/values to update
            inferenceModelKey = ""
            inferenceModelVal = 0
            if key == "AGE":
               inferenceModelKey = key
               inferenceModelVal = (float(body[key]) - 43.65052) / 14.989378

            elif key == "WKSWORK1":
               inferenceModelKey = key
               inferenceModelVal = (float(body[key]) - 47.11975) / 12.422507

            elif key == "UHRSWORK":
               inferenceModelKey = key
               inferenceModelVal = (float(body[key]) - 38.89632) / 12.446644

            elif key == "TRANTIME":
               inferenceModelKey = key
               inferenceModelVal = (float(body[key]) - 20.862526) / 22.125769

            elif type(body[key]) == list:
               for val in body[key]:
                  updateKeysAndValues(val, 1)
               continue
                     
            else:
               inferenceModelKey = body[key]
               inferenceModelVal = 1

            updateKeysAndValues(inferenceModelKey, inferenceModelVal)
               


               

            allFieldsList = list(allFields.values())
            notProtectedFieldsList = list(notProtectedFields.values())
            protectedFieldsList = list(protectedFields.values())

            allFieldsOutput = allFields_net(torch.tensor(allFieldsList, dtype=torch.float32))
            notProtectedFieldsOutput = notProtectedFields_net(torch.tensor(notProtectedFieldsList, dtype=torch.float32))
            protectedFieldsOutput = protectedFields_net(torch.tensor(protectedFieldsList, dtype=torch.float32))
            
         

         return {
            "allFields": allFieldsOutput.item(),
            "notProtectedFields": notProtectedFieldsOutput.item(),
            "protectedFields": protectedFieldsOutput.item()
            }
   
   if request.method == "GET":
       return "GET request received"



   return "Running inference"



'''
 note: 
    This if statement is only true if you run this file directly (ie. locally).
    When running this project on azure, it will be false because the deployment 
    script does not do "python app.py", it does "gunicorn app:app" instead 
    (the format is {module_import}:{app_variable} where module_import is 
    module/filename with your application and app_variable is the variable with 
    the Flask application var).

 '''
if __name__ == "__main__":
    # set logging level to DEBUG if running it locally (not on azure)
    logging.basicConfig(level=logging.DEBUG)

    # run app locally
    app.run(port=8000)