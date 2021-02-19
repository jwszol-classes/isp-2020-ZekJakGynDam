curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt-get install unzip
unzip awscliv2.zip
sudo ./aws/install
rm awscliv2.zip
rm -r -f ./aws
mkdir ~/.aws
touch ~/.aws/credentials
touch ~/.aws/config
(echo -e [default]; echo region = us-east-1; echo output = json) > ~/.aws/config

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

python airplanes_dynamodb_tables_creator.py