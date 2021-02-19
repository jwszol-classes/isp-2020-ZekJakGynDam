mkdir get_pip
curl https://bootstrap.pypa.io/get-pip.py -o get_pip/get-pip.py
python3 get_pip/get-pip.py
rm -r -f get_pip/
python3 -m pip install virtualenv
cp .vimrc ~/.vimrc

python3 -m virtualenv venv
source venv/bin/activate

git clone https://github.com/openskynetwork/opensky-api
cd opensky-api/python
python setup.py install
cd ../..
rm -r -f opensky-api/

pip install -r requirements.txt