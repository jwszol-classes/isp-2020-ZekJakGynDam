# Airplanes

### Setup

Create virtual environment:
```
python -m virtualenv venv
cd venv/Scripts/activate
```

#### Setup Opensky-API
Create account on opensky-api:
https://opensky-network.org/index.php?option=com_users&view=registration

Install opensky-api:
```
git clone https://github.com/openskynetwork/opensky-api
cd opensky-api/python
python setup.py install
cd ../..
```

#### Setup Geoapify
Create account on geoapify:
https://myprojects.geoapify.com/login

#### Setup Basemap

##### Windows

* Download **basemap‑1.2.2‑cp39‑cp39‑win_amd64.whl** file from following link https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap and save it in project main directory.
* write following command in cmd:
```
pip install basemap‑1.2.2‑cp39‑cp39‑win_amd64.whl
```

#### Credentials

Prepare credentials.json file in main project directory by duplicate credentials_default.json and changing its name (don't add this file to repository!). Fill places with your registrations and api keys data


### Run
```
python opensky_test.py
python geoapify_test.py
python visualisation.py
```
