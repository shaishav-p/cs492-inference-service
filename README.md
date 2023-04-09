# CS 492 Inference Service
This Python back-end application was created as part of the final project for CS492 (Social Implication of Computing) W23. Our final project's aim was to understand how biases can exist in ML models and to explore ways in which we can prevent biases in ML models.


## About the Project
We trained multiple dense neural networks to predict income, with each neural network given different subsets of input.  The first was given all inputs, the second was given everything except “protected fields” (which we defined as anything that would be considered discriminatory if used by humans to make salary determinations), and the third was given only protected inputs (in other words, it was trained to be a “stereotype bot”). We predicted that the model would learn biases even without being given protected fields through proxy variables. Therefore, we had 3 goals. The first was to evaluate what biases, if any, were present in the main model. The second was to see what, if any, effect removing the protected fields had on these biases by comparing the main and no protected models. The third was to see if a model trained only on protected fields could be better than random chance, and if so, what it could show us about how machine learning models can learn biases. The repository for training these ML models can be found [here](https://github.com/jhargun/AI-Bias-Experiment).

The results of the ML models and findings from the project can be viewed at [https://cs492-project-woad.vercel.app/](https://cs492-project-woad.vercel.app/). The repository for this frontend website can be found [here](https://github.com/vicswu/CS492-Project). 

This Python backend service was created to the support the "TRY IT YOURSELF" feature on the frontend website which allows users to input their own information through a form on the website, and see how our three different models would predict their salary. Specifically, this Python backend service enables this by running inference on all three models using PyTorch and the user-submitted data from the front-end form.


## Accessing the Service from the Cloud
This service has also been deployed on Azure ([https://cs492-inference-service.azurewebsites.net/](https://cs492-inference-service.azurewebsites.net/)) with a basic CD pipeline setup, whereby any code changes to this repository's master branch are automatically picked up, built, and deployed to the service running on Azure. 


## Usage
This service accepts requests at `/run-inference` where the body must contain the required parameters (e.g. age, gender, race, occupation, education, state, etc.) for our three trained ML models (i.e. the *.pt files in this repository). Upon receiving a request, the service will parse the data in the request body, and use it as input parameters to run inference on the three ML models. The results from all three models will be returned in the response body (in JSON format) 

## Requirements
If you do not already have Python 3.10.x installed, then please install it from [here](https://www.python.org/downloads/) .
<br/>
<br/>

## Getting Started (Locally)
First, install the library dependencies for this project:

```pip install -r requirements.txt```

Next, run this project as a development server: 

```python3 app.py```

Alternatively, to run this project as a production server:

```gunicorn app:app```

To verify that the service is running, send a GET request to this test/health-check endpoint [http://localhost:8000/](http://localhost:8000/) with your browser or another method (e.g. curl, Postman etc.).

