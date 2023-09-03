## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [django-tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## Install and Run

You need to install the necessary dependencies for this project
1. Install [Python](https://www.python.org/downloads/).
2. Use the following command to install necessary dependencies.
```
pip install -r requirements.txt 
``` 
3. Install python virtual environment.
```bash
python -m pip install --user virtualenv
```
4. Run this command to anable virtual environment.
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
 5. Run the program.
```
python .\manage.py runserver
```
  6. If you want to exit the program simply hit ctrl+c to deactivate django server and use 
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

