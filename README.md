# sie-backend

The repository contains code for backend infrastructure of Self Image Experiment (SIE) web-application using Google Cloud Platform. The following sections below will provide you more information on how to setup the local environment.

## Setup development environment

To setup your local env, you will need to install Python 3.6+ and Google SDK in a UNIX based operating system.

- ### Clone the repository

  ```
  $ git clone https://github.com/neu-self-image-experiments/sie-backend.git
  ```

- ### Installing dependencies

  If you do not have `venv` package you can first install it:

  ```
  $ sudo apt install python3-venv
  ```

  Then to create new virtual environment run the following command in your project directory:

  ```
  $ sudo python3 -m venv venv
  ```

  You need to activate the virtual environment in order to use it. So activate the virtual environment using the following command:

  ```
  $ source venv/bin/activate
  ```

  Once activated, you would see the shell prompt will change and it will show the name of the virtual environment that you are currently using. In our case it is venv.

  Now install all the dependencies using:

  ```
  (venv) $ sudo pip3 install -r requirements.txt
  ```

  Now run the flask server:

  ```
  (venv) $ python3 main.py
  ```

* ### Installing Google SDK

  To install Google Cloud SDK for your OS: https://cloud.google.com/sdk/docs/install#installation_instructions

* ### Deploying function to Google Cloud

  Using the gcloud command-line tool, deploy your function from the directory containing your function code with the gcloud functions deploy command:

  ```
  gcloud functions deploy FUNCTION_NAME --runtime python37 --trigger-http --allow-unauthenticated
  ```

  Note: <i> For more information please check - https://cloud.google.com/functions/docs/deploying/filesystem#python_example </i>

## Testing

- ### Test Python Google Cloud Functions on Your Local Development Environment

  Using the Functions Framework for Python to debug and test how your HTTP-functions behave before deploying them to the Google Cloud Platform

  1. Create a .env.local environment file in the Scripts directory
  2. Define function name and a port number in this file

  ```
      export FUNCTION_NAME_HTTP=[name of the function to test]
      export FUNCTION_PORT_HTTP=4000
  ```

  3. Create run-local-script.sh script in the scripts directory

  ```
  #! /bin/bash

  DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
  SOURCE_FILE="${DIR}/../src/main.py"

  source "${DIR}/.env.local"

  functions-framework \
      --source=${SOURCE_FILE} \
      --target=${FUNCTION_NAME_HTTP} \
      --signature-type=http \
      --port=${FUNCTION_PORT_HTTP} \
      --debug
  ```

  - This script pass ../src/main.py as the --source argument
  - Loads the environment variables from the .env.local file
  - Makes use of the FUNCTION_NAME_HTTP environment variable to define what’s the target function to be served with the --target argument
  - Specifies the --signature-type is http
  - Make use of the FUNCTION_PORT_HTTP environment variable to define at which port it should listen to with the -- port argument
  - Enable debugging with --debug


    4. Create test-local-script.sh script in the scripts directory

    ```
    #! /bin/bash

    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    SOURCE_FILE="${DIR}/../src/main.py"

    source "${DIR}/.env.local"

    curl "http://localhost:${FUNCTION_PORT_HTTP}/?subject=[pass the parameter value to test here]"
    echo
    ```
    - This script loads the environment variables defined at .env.local
    - issues a GET HTTP request to localhost at the port identified by the FUNCTION_PORT_HTTP environment variable
    - and pass [the parameter value to test here] as the value to the subject query string parameter

    5. ```cd scripts```
    6. Enter ```chmod +x run-local-script.sh``` to give it executable access.
    7. Enter ```chmod +x test-local-http.sh``` to give it executable access.
    6. Pass this command on the terminal ```./run-local-http.sh``` . This makes sure that the function is being served at the port 4000 defined by FUNCTION_PORT_HTTP environment variable sourced from the .env.local file
    7. Open a new terminal on the side and pass the command ```./test-local-http.sh ```. This will run the function to be tested.

## Contribution policy

### Branching and Merging

When working out on a new feature or fix, checkout out to the `master` branch and pull the new code from the remote repository:

```
$ git checkout master
$ git pull
```

Once you do this, create a new branch by running

```
$ git checkout -b feature/PROJECT-#-short-label

OR

$ git checkout -b hotfix/PROJECT-#-short-label
```

The `PROJECT` and `#` should match the project code and Jira ticket number you are currently on, like `SIE-4-create-cloud-function`; this will let your teammates know which feature your working on and review your work against the JIRA ticket number.

When your work is ready, open a PR into `master` and select **<u>at least one teammate</u>** (ideally it should be the issue reporter) to review your work. Please format the PR title like this: `SIE-XX Description`, this will link your PR to the corresponding JIRA task. If you run into conflicts, resolve them before passing your work onto someone else for review. Once your PR has been approved, it can be merge into the `master` branch and be integrated into the code base.

Whenever a PR is approved, make sure you delete your branch to keep the repo clean and organized.

Try to keep your PR short since it will be faster and easier for the reviewer to give appropriate feedback. Otherwise try to divide the task into sub tasks and follow.

### Code Review guidelines

Reviewers are expected to actually take time to inspect the reviewee's work and flag any potential issue and/or oversight included in the branch. Similarly reviewees are expected to aknowledge any feedback and make adjustments accordingly. Since the PR might be acting as a blocker for other team members, please be mindful and do code reviews as soon as possible (ideally within 24 hours).

## Test Guidelines

### Prerequisite

Please write unit tests into the target function's folder and name it test.py. If test.py already exist, just add your unit tests into the file.

In order to do the unit test, functions-framework should be installed initally. You can run the following command to install functions-framework

```
pip install functions-framework
```

For more information regarding functions-framework please refer to: https://github.com/GoogleCloudPlatform/functions-framework-python

Also, please make sure you already have a credential file inside env/ folder. For setting environment variable please refer to: https://cloud.google.com/docs/authentication/getting-started#setting_the_environment_variable

### Creating your unit test

For more information regarding writing a unit test, please follow the guidlines on Testing HTTP Functions for unit test: https://cloud.google.com/functions/docs/testing/test-http#unit_tests

You can run your test with following commmand (Please make sure you are in the right directory)

```
functions-framework --source=test.py --target=THE_NAME_FOR_UNIT_TEST_FUNCTION
```

### Sending a HTTP request

Finally, make a HTTP request to default address http://0.0.0.0:8080 via Postman. You can also send parameter with a HTTP request.

For more information about how to use Postman or how to pass paramter with a HTTP request via Postman, please refer to: https://learning.postman.com/docs/sending-requests/requests/

<hr>

## Quick Links

JIRA board: [here](https://cs6510.atlassian.net/secure/RapidBoard.jspa?rapidView=4&projectKey=SIE&selectedIssue=SIE-5)

Confluence Page: [here](https://cs6510.atlassian.net/wiki/spaces/SIE/pages/16941064/Project+Primer)

<hr>

### Learning Resources

- Cloud Functions Tutorial: https://cloud.google.com/functions/docs/first-python
- Python Quickstart: https://cloud.google.com/functions/docs/quickstart-python
- More on Python + GCF: https://medium.com/@timhberry/getting-started-with-python-for-google-cloud-functions-646a8cddbb33
- Image recognition with GCF: https://www.serverless.com/blog/google-cloud-functions-application
- More on serverless and GCF: https://www.serverless.com/framework/docs/providers/google/guide/functions/
- Testing functions: https://medium.com/ci-t/how-to-develop-debug-and-test-your-python-google-cloud-functions-on-your-local-dev-environment-d56ef94cb409
