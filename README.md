# SurveysAPI

This project is a simple API built using Python/Django REST Framework for storing data about surveys and responses to surveys.

## Setup
- Install [Python](https://www.python.org/downloads/) (3.x)

- Clone this repository

- Install python dependencies
```
>>pip install -r requirements.txt
```

- Initialise database
```
>>python manage.py makemigrations surveys
>>python manage.py migrate
```
>As this is a demonstrator project focused on the building of the API, Django's in-built SQLite database has been used.
For details of setting up a django project with other databases, see the [Django documentation](https://docs.djangoproject.com/en/2.2/topics/install/#database-installation).

- Run tests
```
>>python manage.py test
```

- Run application
```
>>python manage.py runserver
```
>The API is now running on localhost:8000 - for details of how to interact with the API, see the following documentation

## Endpoints
### GET /api/surveys/
#### Description
Returns a list of all existing surveys
#### Query parameters
> **user**: *int* Filters list of surveys by user_id
#### Examples
List all surveys in database
```
>>curl -XGET "http://localhost:8000/api/surveys/"

HTTP 200 OK
[
    {
        "id": 1,
        "survey_name": "survey1",
        "available_places": 1,
        "user_id": 1
    },
    {
        "id": 2,
        "survey_name": "survey2",
        "available_places": 1,
        "user_id": 2
    },
    {
        "id": 3,
        "survey_name": "survey3",
        "available_places": 1,
        "user_id": 2
    }
]
```
<br>List all surveys for a given user
```
>>curl -XGET "http://localhost:8000/api/surveys/?user=2"

HTTP 200 OK
[
    {
        "id": 2,
        "survey_name": "survey2",
        "available_places": 1,
        "user_id": 2
    },
    {
        "id": 3,
        "survey_name": "survey3",
        "available_places": 1,
        "user_id": 2
    }
]
```

### POST /api/surveys/
#### Description
Creates a new survey
#### Parameters
>**survey_name**: *str* Name of the survey

>**available_places**: *int* Maximum number of survey responses allowed

>**user_id**: *int* Owning user of the survey
#### Errors
400 Bad Request: Required parameters missing or invalid
#### Examples
```
>>curl -XPOST "http://localhost:8000/api/surveys/" -d "survey_name=survey1&available_places=1&user_id=1"

HTTP 201 Created
{
  "id": 1,
  "survey_name": "survey1",
  "available_places": 1,
  "user_id": 1
}
```
### GET /api/survey-responses/
#### Description
Returns a list of all existing survey responses
#### Query parameters
> **user**: *int* Filters list of survey responses by user_id

> **survey**: *int* Filters list of survey responses by survey_id
#### Examples
List all survey responses in database
```
>>curl -XGET "http://localhost:8000/api/survey-responses/"

HTTP 200 OK
[
    {
        "id": 1,
        "survey_id": 1,
        "user_id": 2,
        "created_at": "2019-11-27T17:41:27.205398Z"
    },
    {
        "id": 2,
        "survey_id": 2,
        "user_id": 1,
        "created_at": "2019-11-27T17:41:46.787398Z"
    },
    {
        "id": 3,
        "survey_id": 3,
        "user_id": 1,
        "created_at": "2019-11-27T17:42:14.518398Z"
    }
]
```
<br>List all survey responses belonging to a given user
```
>>curl -XGET "http://localhost:8000/api/survey-responses/?user=1"

HTTP 200 OK
[
    {
        "id": 2,
        "survey_id": 2,
        "user_id": 1,
        "created_at": "2019-11-27T17:41:46.787398Z"
    },
    {
        "id": 3,
        "survey_id": 3,
        "user_id": 1,
        "created_at": "2019-11-27T17:42:14.518398Z"
    }
]
```
<br>List all responses to a given survey
```
>>curl -XGET "http://localhost:8000/api/survey-responses/?survey=2"

HTTP 200 OK
[
    {
        "id": 2,
        "survey_id": 2,
        "user_id": 1,
        "created_at": "2019-11-27T17:41:46.787398Z"
    }
]
```

### POST /api/survey-responses/
#### Description
Creates a new survey response
#### Parameters
>**survey_id**: *int* Survey to respond to

>**user_id**: *int* Owning user of the survey response
#### Errors
400 Bad Request: Required parameters missing or invalid

403 Forbidden: No remaining spaces available on survey

404 Not Found: No survey found with ID specified
#### Examples
```
>>curl -XPOST 'http://localhost:8000/api/survey-responses/' -d "survey_id=1&user_id=2"

HTTP 201 Created
{
    "id": 1,
    "survey_id": 1,
    "user_id": 2,
    "created_at": "2019-11-27T17:41:27.205398Z"
}
```
