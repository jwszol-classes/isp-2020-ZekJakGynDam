mkdir Projects
cd Projects

install pip for python3

mkdir get_pip
curl https://bootstrap.pypa.io/get-pip.py -o get_pip/get-pip.py
python3 get_pip/get-pip.py
python3 -m pip install virtualenv

git clone git@github.com:jwszol-classes/isp-2020-ZekJakGynDam.git
cd isp-2020-ZekJakGynDam/
cp .vimrc ~/.vimrc

python3 -m virtualenv venv
source venv/bin/activate

git clone https://github.com/openskynetwork/opensky-api
cd opensky-api/python
python setup.py install
cd ../..
rm -r -f opensky-api/

pip install boto3
pip install bs4