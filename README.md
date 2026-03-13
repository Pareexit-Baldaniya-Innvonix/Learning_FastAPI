# FastAPI
Learning and completing all FastAPI tasks in this repository.

## How to run the code
For running the code need to add `uvicorn` and then need to follow this steps:
1. open terminal
2. set the file url to that place where main file located
3. run this code 
    
    Terminal-1:
    - `uvicorn main:app --host 127.0.0.1 --port 8000 --reload`
    - --reload - used for auto reload the file

    Terminal-2:
    - `python test_api.py`
    - this runs a loop which checks how many requests are allowed and what happens after rate-limit hits.