# cs492-inference-service
Python back-end application for CS492 W23





## Requirements

If you do not already have Python 3.10.x installed, then please install it from [here](https://www.python.org/downloads/) .

## Getting Started
First, install the library dependencies for this project:

```pip install -r requirements.txt```

Next, run this project as a development server: 

```python3 app.py```

Alternatively, to run this project as a production server:

```gunicorn app:app```


To verify that the service is running, send a GET request to this test/health-check endpoint [http://localhost:8000/](http://localhost:8000/) with your browser or another method (e.g. curl, Postman etc.).
