# analytics-microservice

## Setup

### Install prerequisites

```shell
pip install -r requirements.txt
```

### Run the app

```shell
uvicorn src.main:app --reload
```

By default, it runs on http://127.0.0.1:8000

### Run tests

#### All tests

```shell
pytest
```

#### A specific test

```shell
pytest -k <test_name>
```

For example, `pytest -k test_main`

