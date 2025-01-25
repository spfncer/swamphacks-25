# Backend

## Installation & Execution

First, create a `.env` file within the `/backend` directory, following the strucutre of the `sample.env` file. 
Add the appropriate fields to the `.env` file to point to your MongoDB instance.

To install dependencies of the FastAPI server, run the following commands within the `/backend` folder:
```
pip install -r requirements.txt
```

To run the FastAPI server, execute the following command from within the `/backend/src` folder: 
```
fastapi dev main.py
```

To install dependencies of the FastAPI server unit tests, run teh following command within the `/backend` folder:
```
pip install -r requirements.dev.txt
```

To run the project's unit tests, execute the following command from with in the `/backend` folder:
```
python -m pytest test
```
