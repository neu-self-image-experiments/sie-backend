## Cloud Function for Fetching Qualtrics Responses

This cloud function is responsible for catching qualtrics responses. At the end of each qualtrics survey, a qualtrics POST action is executed which sends a POST request to this function's endpoint. This function then parses the request and modifies the corresponding user data.

### Testing

- Unit Test

    ```
    cd qualtrics_server
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    pip install -r requirements-test.txt
    pytest test.py
    ```