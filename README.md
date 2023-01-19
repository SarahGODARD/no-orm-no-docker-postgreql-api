# Description

This is a simple API in a bank context.

## Dependencies

- postgresql
- python
- flask
- apidoc
- pytest

## Run the environnement

To get the environement set up:

 ```
source my_env/bin/activate
```

## Initialise the data base

 ```
sudo service postgresql start
```

```
sudo -iu postgres psql
```

```
CREATE DATABASE bank_db;
```

```
CREATE USER someone WITH PASSWORD 'password';
```

```
GRANT ALL PRIVILEGES ON DATABASE bank_db TO someone;
```

```
\q
```

 ```
python init_db.py
```

## Run the API

To start the API usage:

 ```
flask run
```

See the documentation running : apidoc/index.html

## Tests

 You must got pytest.

  ```
pytest src/test.py
```

## Documentation

To update the documentation, fill the different comment section of apidoc and run :

 ```
apidoc -i src -o apidoc
```

## Credits

GODARD Sarah