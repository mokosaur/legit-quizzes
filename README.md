# legit-quizzes
A web platform that allows users to make quizzes which will gather information from other users, and then if there is sufficient data provided, a classifier can be produced. This classifier is based on statistics and machine learning methods, and gives detailed information about the result.

## Requirements
- Python 3.5
- Django 1.8
- psycopg2 (or other library if you want to replace the PostgreSQL database)
- scikit-learn 0.17
- scipy 0.17
- numpy 1.11
- selenium (along with the driver for your browser, only for tests)

## How to run this
Clone this repository, and navigate to the main directory. Type in the command
```
python manage.py runserver
```
The application will be available at localhost:8000 or different default port if this one is occupied.

If you see an error message, you probably do not have your database running or should be configured (see next section). If you have an empty database you should run these two commands:

```
python manage.py makemigrations
```
```
python manage.py migrate
```

## Database configuration
You can change your database and fill in your username nad password in `settings.py` at the line that starts with `DATABASES`. More details [here](https://docs.djangoproject.com/en/1.11/ref/databases/).
