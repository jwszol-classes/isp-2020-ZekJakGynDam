# Airplanes
Project with use of AWS that is used to visualize airplanes that are located in Poland.
This branch is used as simplified version of entire project.

## Setup
Create virtual environment:
```
python -m virtualenv venv
cd venv/Scripts/activate
```

### Setup OpenSky-API
Create account on OpenSky-api:
https://opensky-network.org/index.php?option=com_users&view=registration


### Setup Mapbox
Create account on Mapbox:
https://www.mapbox.com/maps/


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
* go to repository directory
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
* install requirements
```
pip install boto3
pip install bs4
```


#### Instance setup - create image
* go to EC2 service
* click **Instances (running)**
* click right mouse button on instance
* choose **Image and templates**
* choose **Create image**
* provide **Image name** (for example "airplanes_image")
* uncheck **Delete on termination** checkbox
* click **Create image**
* go to EC2 service
* go to Images/AMIs
* wait until **Status** of your image change into "available" (don't terminate instance until then!!!)


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
* go to Kinesis service
* choose **Create data stream**
* provide **Data stream name** (for example "airplanes_stream")
* provide **Number of open shards** as 1
* click **Create data stream**


### AWS Lambda
#### Creating Lambda Function 
* go to Lambda service
* click **Create function**
* choose **Author from scratch**
* provide **Function name** (for example "airplanes_lambda_function")
* provide Runtime (**Python 3.8**)
* expand **Change default execution role** and remember execution role name assigned to lambda function (for example "airplanes_lambda_function-role-16dg8abt")
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
* click **Create policy**
* choose **JSON**
* paste following code into input text
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:340900857390:table/*"
        }
    ]
}
```
* click **Review policy**
* provide name of policy (for example "AWSLambdaMicroserviceExecutionRole")
* click **Create policy**
* click **Create policy**
* choose **JSON**
* paste following code into input text
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:340900857390:table/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "arn:aws:lambda:us-east-1:340900857390:function:*"
        }
    ]
}
```
* click **Review policy**
* provide name of policy (for example "AWSLambdaTestHarnessExecutionRole")
* click **Create policy**
* search and check **AmazonKinesisFullAccess** and two earlier created policies
* click **Attach policy**
* go back to trigger configuration tab and click **Add**


#### Adding resources
* go to isp-2020-ZekJakGynDam\aws_lambda directory
* zip all files in this directory into .zip archive (for example "aws_lambda.zip")
* in lambda function page click on **airplanes_lambda_function**
* Under **Function code** section click **Actions**
* choose **Upload a .zip file**
* find and save "aws_lambda.zip"
* go under **Runtime settings** settings and click **Edit**
* change Handler into "airplanes_lambda_function.airplanes_lambda_handler"
* click **Save**


#### Configuration
* go under **Basic settings** section and click **Edit**
* set **Memory (MB)** as 1024
* set **Timeout** as 30 sec
* click **save**

#### Congratulations
You have just configured AWS Lambda function for checking if airplane is above Poland and updating DynamoDB tables! Congratulations.

### Local machine configuration
#### Linux Ubuntu
Configuration is similar to the one described in **EC2** section

#### Windows
* download AWS installer from:
 https://awscli.amazonaws.com/AWSCLIV2.msi
 and install it
* create folder for AWS credentials file in following path:
```
C:\Users\USER
```
where "USER" is user name
* open labs.vocareum page
* click **Account Details**
* click **show**
* copy showed text
* paste it into 
```
C:\Users\USER\.aws\credentials
```
* paste following text 
```
[default]
region = us-east-1
output = json
```
into
```
C:\Users\USER\.aws\config:
```

* run following command in virtual environment
```
pip install -r requirements.txt
```

### Credentials
Prepare credentials.json file in main project directory by duplicate credentials_default.json and changing its name (don't add this file to repository!). Fill places with your registrations, access tokens data, aws vocareum cookies data etc.

## Run
On EC2 instance run to read airplanes data:
```
python Kinesis_airplanes_test\producer.py
```
On local machine run to visualization airplanes:
```
python visualisation_animation_basemap.py
```
or
```
python visualisation_animation_plotly.py
```
In second case open following url link in browser:
```
http://127.0.0.1:8050/
```
