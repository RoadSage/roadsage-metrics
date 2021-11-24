# Roadsage - Metrics API

An API to collect and store sensor data and usage metrics from the Roadsage app and display. It is created using the [FastAPI framework](https://fastapi.tiangolo.com/).

## Installation

Dependencies are managed using [Poetry](https://python-poetry.org/).

```sh
# to install all packages
poetry install

# to open a virtual enviroment to run commands
poetry shell

# to export dependencies to requirements.txt for other tools run
poetry export -f requirements.txt --output requirements.txt
```

## Linting

The code is formatted using the `black` formatter, to ensure consistency and readablility.
`isort` is used to format and sort import statements in a regular way.
The code is written using python typehints to provide better editor experience and catch errors using the `mypy` type-checker.

```sh
# to reformat all the code run
black .

# to reorder imports run
isort .

# to check that the code matches the format run
black . --check

# to check imports are in the correct order run
isort . --check-only

# to typecheck the code run
mypy
```

## Testing

Unittests are in the `/tests` directory and are run using pytest. To run all the tests and gather test coverage:

```sh
coverage run -m pytest
coverage html
coverage report --skip-empty
```

## Usage

#### Single Sign On Data

Sign in via Google is supported, it needs the relevant Google credentials for this to work.
You can set this up in the [Google Developer Console](https://console.developers.google.com/apis/credentials).

The credentials are read from a `.env` file, it should contain a GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.

Run the following command and fill in the details in the `.env` file:

```sh
cp .env.sample .env
```

#### Secret Key

The passwords are hashed and the app expects the a secret key to be stored in the APP_SECRET_KEY enviroment variable.

To generate a secret key run:

```sh
openssl rand -hex 32
```

and store the result in the APP_SECRET_KEY environment variable.

```sh
set APP_SECRET_KEY=<secret key generate with command above>
```

#### Start Server

To run the app with reloading enabled for development run:

```sh
uvicorn src.main:app --reload
```

FastAPI automatically documents the available API routes and generates automatic documentation which can be viewed by going to `/docs` or `/redoc`.
