# Analytics Microservice

## Brief overview of the project
This project is to build APIs for BU SAIL's analytical microservice. Due to privacy protection rule (HIPAA), BU SAIL is unable to use existing analytical services, so we are building APIs that are albe to store and retrieve information of users that interact with BU SAIL, and BU SAIL can deploy our APIs to their microservice to have their own analytical microservice. Because our APIs will manage the users data in BU SAIL's private database, so BU SAIL's  analytical microservice which runs our APIs will follow the privacy protection rule. Our APIs can be called to collect a user's information of session, event(screen scrolling, mouse clicking, etc), screen, and retrieve information such as daily/weekly/monthly active users, average active time of a user, the event that he did, screen that he visits, and the time he spent on a specific screen.

## Technical architecture and explanation
<img width="705" alt="Screenshot 2023-05-04 at 5 12 40 PM" src="https://user-images.githubusercontent.com/36748450/236333635-cd2c5002-2f09-4cce-a564-91132b1fef0c.png">   
Explanation:   <br>     
The application is a FastAPI that contains the APIs we wrote. The FastAPI is treated as a microservice and ran using uvicorn. The FastAPI’s endpoints will store and retrieve data from a MySQL database by using an ORM called SQLAlchemy. Clients use our application’s APIs by sending HTTP Request.



## Issues of current project
1. (session.py)"delete_session_from_database" function shows mapping error https://github.com/hicsail/analytics-microservice/issues/22
3. add database connection string to GitHub Secrets for CI https://github.com/hicsail/analytics-microservice/issues/15

## Deployment
see https://github.com/hicsail/analytics-microservice/blob/main/DEPLOYMENT.md

## Detailed instructions on how to run our project

### Install virtual requirement
1. create a python environment named env  
```shell
python3 -m venv env
```
2. Activate the virtual environment by running the following command:
```shell
source env/bin/activate
```
3. Now you will use this environment to install the prerequisites of this application and run this application.
4. Deactivate the virtual environment after you are done by running the folloing command:
```shell
deactivate
```
5. (Optional) If you want to delete the virtual environment you installed, run the follwing command:
```shell
rm -rf ~/env
```

### NOTE: Do all the following step in the virtual environment you just installed above.
### Install prerequisites

```shell
pip install -r requirements.txt
```
### Set environment variables

Create a .env file in the root directory and add the following variables:

```shell
DB_CONNECTION_STRING=mysql+pymysql://username:password@hostname:port/database_name
```

### Run the app

```shell
uvicorn src.main:app --reload
```

By default, it runs on http://127.0.0.1:8000 and you will see the response:

```json
{
  "message": "The analytics service is running."
}
```

### Run tests

#### All tests

```shell
pytest
```

#### A specific test

```shell
pytest -k <test_file_or_function>
```

For example, `pytest -k test_main`

