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

Create account on opensky-api:
https://opensky-network.org/index.php?option=com_users&view=registration

Create account on geoapify:
https://myprojects.geoapify.com/login

Prepare credentials.json file in main project directory by duplicate credentials_default.json and changing its name (don't add this file to repository!). Fill places with your registrations and api keys data


### Run
```
python opensky_test.py
python geoapify_test.py
```
