# Airplanes

### Setup

Create virtual environment:
```
python -m virtualenv venv
cd venv/Scripts/activate
```

Install opensky-api:
```
git clone https://github.com/openskynetwork/opensky-api
cd opensky-api/python
python setup.py install
cd ../..
```

Prepare credentials.json file in main project directory (don't add this file to repository!):
```
{
    "username" : "username",
    "password" : "password"
}
```

### Run
```
python opensky_test.py
```
