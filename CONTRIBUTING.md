# Development
Untitled is a web application with server written in Python, its server side is currently developed using the Flask framework.
## Using Python
We are currently using Python3.8, Flask requires at least Python 3.7 to function properly. Please make sure you have up-to-date Python installed.
## Getting the code
1. Make sure you have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed
2. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the repository
3. Clone your fork
4. Fetch and checkout the "dev" branch to work on, you can also create new branches as needed.
## Setting up virtual environment
### Using linux:
1. ` $ cd ` into the project repository
2. Run```$ Python3 -m venv .venv```to create a virtual environment
3. When the virtual environment setup is complete, run```$ source .venv/bin/activate```
4. You should see (.venv) in your terminal.
## Working with dependencies
1. Make sure you are running the correct virtual environment. Run`$ pip freeze`to check what's currently installed. You should see nothing.
2. Run `$ pip install -r requirements.txt` to install dependencies. Note: You might need to use `pip3`
3. If you want to add dependencies, remember to use `$ pip freeze > requirements.txt` to add new libraries.
## Debugging Locally
1. If flask and dependencies are installed in a virtual environment, activate the virtual environment before proceeding.
2. ```$ export FLASK_APP=app```
3. ```$ export FLASK_DEBUG=True``` This enables rerunning the server upon edit, skip this step if the feature is unnecessary.
4. ```$ flask initdb``` to initialize the SQLite database, this only need to happen once unless `models.py` is modified. You might have to manually delete the db.sqlite file and excute this step again to reset the database.
5. ```$ flask run``` to start the server, the link to open a browser will be displayed in the console. 
6. To avoid bugs with virtual environments in the future, run `$ deactivate` when finished.
## Coding style guide
Currently we follow the [PEP8](https://peps.python.org/pep-0008/) style guide for all Python code in this repository.
## Submit PRs
- It is recommended, but not enforced, that contributors should open a issue first, then submit the PR
- Submit PRs frequently, try to avoid large chunks of code in one PR.

