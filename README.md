## KU Polls: Online Survey Questions 
[![Unit Tests.](https://github.com/GGWPXXXX/ku-polls/actions/workflows/python-package.yml/badge.svg)](https://github.com/GGWPXXXX/ku-polls/actions/workflows/python-package.yml)
[![Flake8](https://github.com/GGWPXXXX/ku-polls/actions/workflows/flake8.yml/badge.svg)](https://github.com/GGWPXXXX/ku-polls/actions/workflows/flake8.yml)

An application to conduct online polls and surveys based
on the [django-tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run

You need to install the necessary dependencies for this project
1. Install [Python](https://www.python.org/downloads/).

2. Install python virtual environment.
```
python -m pip install virtualenv 
```

3. Create a new `.env` file in the project's root directory. You can use a text editor of your choice to create and edit the file.

4. Add the following configuration settings to the `.env` file:

```
SECRET_KEY=your_secret_key_here
```

5. Create new environment.
```
python -m venv venv
```
6. Run this command to anable virtual environment.
```
venv\Scripts\activate
```
But if the program prompted you with an error 
"Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
then use.
```
Set-ExecutionPolicy Unrestricted -Scope Process 
venv\Scripts\activate
```
7. Use the following command to install necessary dependencies.
```
pip install -r requirements.txt 
``` 
8. Run the program.
```
python manage.py migrate
python manage.py loaddata data/polls.json
python manage.py loaddata data/users.json
python .\manage.py runserver
```
  9. If you want to exit the program simply hit ctrl+c to deactivate django server and use 
```
deactivate
```
in your terminal to exit virtual environment.


## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Development Plan](../../wiki/Development%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration-1-Plan)
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)


## Demo Account for User
| Username  | Password        |
|-----------|-----------------|
|   hellodemo1   | passwordisdat |
|   hellodemo2   | passwordisdadadodo |

## Demo Account for Admin
| Username  | Password        |
|-----------|-----------------|
|   admin   | uaregood |
