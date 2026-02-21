<div align="center">

<img src="https://timeweb.com/ru/community/article/9a/9a85b1c113c7e98e491fac0ce67f72f8.jpg" alt="logo" width="270" height="auto" />
<h1>Task Manager</h1>


<p>Hexlet tests and linter status:</p>

[![Actions Status](https://github.com/Dron-N-82/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Dron-N-82/python-project-52/actions)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Dron-N-82_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Dron-N-82_python-project-52)

</div>

# Task manager


### Project description

# Task manager

Task Manager is a task management system similar to [http://www.redmine.org/](http://www.redmine.org/). It allows you to create tasks, assign performers, and change their statuses. Registration and authentication are required to use the system.

### Demonstration project:
[Render "Task Manager"](https://python-project-52-32q5.onrender.com)

### Tools and description:

[uv](https://docs.astral.sh/uv/) — A fast Python package and project manager

[Ruff](https://docs.astral.sh/ruff/) — linter

[Django](https://www.djangoproject.com/) — framework for creating web applications in the Python programming language

[Gunicorn](https://docs.gunicorn.org/en/latest/index.html) — mini web server that runs a Python application

[python-dotenv](https://pypi.org/project/python-dotenv/) — mini web server that manages environment variables by reading key-value pairs from a .env file. This helps in developing applications based on the 12-factor principles, running a Python application

[Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) — cmpiled CSS and JavaScript, it is a powerful and feature-rich front-end toolkit.


## Install

### Clone the repository:

```
git@github.com:Dron-N-82/python-project-52.git

cd python-project-52
```

### To store confidential information, create a .env file in the page-analyzer directory 


```
DATABASE_URL = postgresql://{username}{password}@{host}:{port}/{basename}

SECRET_KEY = "{your_secret_key}"
```

### Install
```
make build
```
### To launch the application, use:
```
make run
```