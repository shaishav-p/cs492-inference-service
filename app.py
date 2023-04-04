import logging
from flask import Flask, request
import constants
import torch
import torch.nn as nn

allFields_inputSize = 573
notProtectedFields_inputSize = 559

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


# allFields_net.load_state_dict(torch.load("allFields_net.pt",map_location=torch.device('cpu')))
allFields_net.load_state_dict(torch.load('allFields_net.pt', map_location=torch.device('cpu')))
notProtectedFields_net.load_state_dict(torch.load('notProtectedFields_net.pt', map_location=torch.device('cpu')))




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

         # get the body of the request
         body = request.get_json()

         # TODO: add validation for request body

         # for key in body:
   
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