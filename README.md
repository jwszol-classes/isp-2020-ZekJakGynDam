# Airplanes

## Setup

Create virtual environment:
```
python -m virtualenv venv
cd venv/Scripts/activate
```

### Setup Opensky-API
Create account on opensky-api:
https://opensky-network.org/index.php?option=com_users&view=registration

Install opensky-api:
```
git clone https://github.com/openskynetwork/opensky-api
cd opensky-api/python
python setup.py install
cd ../..
```

### Setup Geoapify
Create account on geoapify:
https://myprojects.geoapify.com/login


### EC2
#### Generate key pairs
* go to EC2 service
* go to Network & Security/Key Pairs
* click **Create key pair**
* provide **Name** (for example key_test)
* choose **File format** (ppk)
* click **Create key pair**
* download .ppk file into desired directory


#### Launch instance
* go to EC2 service
* click **Launch instance** and choose **Launch instance**
* Choose **Ubuntu Server 20.04 LTS (HVM)** AMI and click **Select**
* choose it.micro Instance Type and click **Review and Launch**
* click **Launch**
* check checkbox and click **Launch Instances**
* click **View Instances**
* copy **Public IPv4 DNS** of your instance (for example "ec2-18-207-187-224.compute-1.amazonaws.com")

#### Connect with instance
* open **PuTTY**
* In **Category** window go to Connection/SSH/Auth and browse for earlier downloaded .ppk key file
* in **Category** window go to Session and fill Host Name (or IP address) inputbox (for example "ubuntu@ec2-18-207-187-224.compute-1.amazonaws.com")
* click **Open**
* on PuTTY Security Alert popup window choose **tak**


#### Instance setup - configure vim
* paste following lines into .vimrc file
```
set nu
syntax on
set autoindent
set tabstop=4
set mouse=a
:colorscheme zellner
```

#### Instance setup - configure AWS
* install AWS
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt-get install unzip
unzip awscliv2.zip
sudo ./aws/install
rm awscliv2.zip
```
* create folder for AWS credentials file
```
mkdir ~/.aws
```
* open labs.vocareum page
* click **Account Details**
* click **show**
* copy showed text
* paste it into ~/.aws/credentials
* paste following text into ~/.aws/config:
```
[default]
region = us-east-1
output = json
```


#### Instance setup - configure git
* write following command with your data:
```
git config --global user.name "full name"
git config --global user.email "email adress"
```
* generate ssh keys:
```
ssh-keygen -o
```
* push **enter** button for each communicate (3 times)
* show public key
```
cat ~/.ssh/id_rsa.pub
```
* log in to **github** service
* go to **Settings**
* go to SSH and GPG keys
* click **New SSH key**
* provide **Title** (for example "ec2_ubuntu_instance") and **Key** (showed earlier public key)
* click **Add SSH key**

#### Instance setup - prepeare repository
* write following commands to create directory for all projects:
```
mkdir Projects
cd Projects
```
* install pip for python3
```
mkdir get_pip
curl https://bootstrap.pypa.io/get-pip.py -o get_pip/get-pip.py
python3 get_pip/get-pip.py
```
* install virtualenv for python3
```
python3 -m pip install virtualenv
```
* download **isp-2020-ZekJakGynDam** repository:
```
git clone git@github.com:jwszol-classes/isp-2020-ZekJakGynDam.git
```
and write "yes" when communicate shows
* got to repository directory
```
cd isp-2020-ZekJakGynDam/
```
* create virtual environment and activate it
```
python3 -m virtualenv venv
source venv/bin/activate
```
* install opensky-api in virtual environment
```
git clone https://github.com/openskynetwork/opensky-api
cd opensky-api/python
python setup.py install
cd ../..
rm -r -f opensky-api/
```
* install boto3
```
pip install boto3
```
#### Instance setup - create image
* go to EC2 service
* click **Instances (running)**
* click right mouse button on instance
* choose **Image and templates**
* choose **Create image**
* provide **Image name** (for example "ec2_ubuntu_instance_airplanes")
* uncheck **Delete on termination** checkbox
* click **Create image**
* go to EC2 service
* go to Images/AMIs
* wait until status of your image change into "available" (don't terminate instance until then!!!)

### Setup Basemap

#### Windows

* Download **basemap‑1.2.2‑cpxx‑cpxx‑win_amd64.whl** file from following link https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap and save it in project main directory.
* write following command in cmd:
```
pip install basemap‑1.2.2‑cpxx‑cpxx‑win_amd64.whl
```
where xx is your python version e.g. 38 for python 3.8
#### Linux

### Kinesis


### AWS Lambda
#### Creating Lambda Function 
* Go to Lambda service
* click **Create function**
* choose **Author from scratch**
* provide **Function name** (for example "lambda_airplanes")
* provide Runtime (**Python 3.8**)
* expand **Change default execution role** and remember execution role name assigned to lambda function (for example "lambda_airplanes-role-p5nao7pr")
* click **Create function**

#### Adding layer with numpy and scipy modules
* click **Layers** and choose **Add a layer**
* choose **AWS layers** ("AWSLambda-Python38-SciPy1x") and **Version** ("29")
* click **Add**

#### Adding Trigger
* click **Add trigger**
* select a **trigger** ("Kinesis")
* choose **Kinesis stream** (name of earlier created stream, for example "stream_airplanes")
* in another tab go to **IAM** service into **Roles**
* search for execution role name assigned to lambda function (for example "lambda_airplanes-role-p5nao7pr") and choose it
* click **Attach policies**
* choose **AmazonKinesisFullAccess**, **AWSLambdaMicroserviceExecutionRole-f5eb932c-ddba-41e0-9d7b-5d88ca96473b**,
**AWSLambdaTestHarnessExecutionRole-b29dfa9b-fcfa-4f5b-a16b-08e2b6ad75ae**
* click **Attach policy**
* go back to trigger configuration tab and click **Add**

#### Adding resources
* go to isp-2020-ZekJakGynDam\aws_lambda directory
* zip lambda_function_airplanes.py and reverse_geocode directory into .zip archive (for example "aws_lambda.zip")
* in lambda function page click on **lambda_airplanes**
* Under **Function code** section click **Actions**
* choose **Upload a .zip file**
* find and save "aws_lambda.zip"
* go under **Runtime settings** settings and click **Edit**
* change Handler into "lambda_function_airplanes.lambda_handler_airplanes"
* click **Save**

#### Congratulations
You have just configured AWS Lambda function for checking if airplane is above Poland and updating DynamoDB tables! Congratulations.

### Credentials
Prepare credentials.json file in main project directory by duplicate credentials_default.json and changing its name (don't add this file to repository!). Fill places with your registrations and api keys data




### AWS


### Communication
* PuTTy
* Xming


## Run
```
python opensky_test.py
python geoapify_test.py
python visualisation.py
```
