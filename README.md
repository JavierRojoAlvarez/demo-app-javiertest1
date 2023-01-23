# Demo App
This is an app built to demonstrate a simple property management system.
It is built using [Django](https://www.djangoproject.com/) web framework for the backend and (pure) HTML/CSS/JS for the front end.

## Getting Started
### Clone
Use Git from the command line or GitHub Desktop to clone this repo. Instructions to clone from GitHub can be found [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository).
### Dependencies
The packages that the demo app relies upon are listed in the `requirements.txt` file.
For Windows, run the following command from within the repo to install the dependencies from this file (within a virtual environment if possible).
```python
pip install -r requirements.txt
```
### Secrets File
Sensitive information - such as the secret key or database credentials - are of course not part of this repo. Instead they live in an untracked file that the `settings.py` module reads. Since it is untracked, this file needs to be created manually. To work correctly it must satisfy the following requirements:

* this file is expected to placed in a directory called `secrets` "one-level above" wherever the repo is located on your computer
* within that directory, the secrets file is expected to be called `secrets-demo-app.json`
This file structure is demonstrated below and it ensures that such a file is completely outside the repo.
```
.
├── secrets
|   ├── secrets-demo-app.json
├── demo-app
    ├── README.md
    ├── base
    ├── node_modules
    ├── package-lock.json
    ├── package.json
    ├── requirements.txt
    └── venv
```
The content of the file itself is just a single object: contact other collaborators to find out more about its structure.
### Database
It is up to the user to configure the database that the app uses and to ensure that the relevant information is correctly contained in the secrets file.

## Usage
### Running the App in Development
Once setup correctly, the app can be run locally on Windows using the following command from the **base directory** of the repo (i.e. where the `manage.py` module is located).
```python
python manage.py runserver
```
By default, the web app can be used by visiting `localhost:8000` in the browser. The user can quit the server with `Ctrl` + `C`.
