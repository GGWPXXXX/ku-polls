# Installation

First you need to install the necessary dependencies for this project

1. Install [Python](https://www.python.org/downloads/).

2. Clone project and Install python virtual environment.

```
git clone https://github.com/GGWPXXXX/ku-polls
```
```
python -m pip install virtualenv
```

3. Create a new `.env` file in the project's root directory. You can use a text editor of your choice to create and edit the file, you can see the sameple in `sample.env`.

```
SECRET_KEY = secret-key-value-without-quotes
DEBUG = False
ALLOWED_HOSTS = *.ku.th, localhost, 127.0.0.1, ::1
TIME_ZONE = Asia/Bangkok
```

4. Create new environment.

```
cd ku-polls
python -m venv venv
```

5. Run this command to anable virtual environment.

```
venv\Scripts\activate
```

But if the program prompted you with an error
"Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"
then use.

```
Set-ExecutionPolicy Unrestricted -Scope Process
```
```
venv\Scripts\activate
```

6. Use the following command to install necessary dependencies.

```
pip install -r requirements.txt
```

7. Run the program.

```
python manage.py migrate
python manage.py loaddata data/users.json
python manage.py loaddata data/polls.json
python .\manage.py runserver
```

8. If you want to exit the program simply hit ctrl+c to deactivate django server and use

```
deactivate
```

in your terminal to exit virtual environment.

# Additional

If you want to see the unit tests of this project simply run,

```
python manage.py test
```
Note : Make sure that when you run test you still in virtual environment.
