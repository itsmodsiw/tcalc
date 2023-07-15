# modsiw's Unix Time Converter


[![Python](https://img.shields.io/badge/Python-3.9-blue)](https://www.python.org/downloads/release/python-390/)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-blue)](https://flask.palletsprojects.com/)
[![pytz](https://img.shields.io/badge/pytz-2021.3-blue)](https://pypi.org/project/pytz/)

Welcome to modsiw's Unix Time Converter! This web application allows you to convert a date and time to a Unix timestamp. It's optimized for `<t:unixtimecode>` for Discord usage.

## Table of Contents
- [Features](#features)
- [Installation and Usage](#installation-and-usage)
- [How to Use](#how-to-use)
- [Accessing the Application](#accessing-the-application)
- [Deploying to Heroku](#deploying-to-heroku)
- [Contributing](#contributing)


## Features
- Convert a date and time to a Unix timestamp.
- Copy the converted timestamp to the clipboard.
- Optimized for `<t:unixtimecode>` for Discord usage.
- Follow modsiw on [Twitter](https://twitter.com/itsmodsiw).

## Installation and Usage
To use modsiw's Unix Time Converter, follow the steps below:

```shell
# Navigate to the project directory
cd your-repo

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Start the Flask development server
flask run
```

## How to Use
Follow these steps to convert a date and time to a Unix timestamp using modsiw's Unix Time Converter:
```shell

Enter a date and time in the provided input fields.

Click the "Convert" button to convert the date and time to a Unix timestamp.

The converted Unix timestamp will be displayed below. Click the "Copy to Clipboard" button to copy the timestamp.

```


## Accessing the Application
To access the application:

```shell
Open your web browser and navigate to http://localhost:5000.

The Unix Time Converter interface will be displayed.

```


## Deploying to Heroku
To deploy the Unix Time Converter application to Heroku, follow these steps:

```shell

Create a new Heroku app.

# Set the necessary environment variables or config vars in Heroku:

FLASK_APP=app.py
FLASK_ENV=production

# Deploy the application to Heroku using your preferred method (e.g., Heroku CLI, Git-based deployment).

Once deployed, access the application using the provided Heroku app URL.

```

## Contributing

```shell

Contributions are welcome! 
```
