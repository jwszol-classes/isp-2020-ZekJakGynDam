# Airplanes
Project with use of AWS that is used to visualize airplanes that are located in Poland.
This branch is used as simplified version of entire project.

### Technologies used and data flow
![diagram](https://github.com/jwszol-classes/isp-2020-ZekJakGynDam/blob/simple_visualization/src/diagram_simple.png)


### AWS EC2 instance
AWS EC2 instance is used for running continuous program that send request to Opensky-Api in order to get data such as:

* ICAO24
* timestamp
* latitude
* longtitude
* heading
* information if airplane is on ground
* velocity

about all airplanes that are currently above geographic bounding box (49.0273953314, 54.8515359564, 14.0745211117, 24.0299857927) (min_latitude, max_latitude, min_longitude, max_latitude) that is based on the extreme geographical points of Poland. These data (together with timestamp of performed request) are then send to Kinesis data stream.

### Kinesis data stream
Kinesis data stream gets data about airplanes and distribute them to different shards, that provide them into AWS Lambda.

### AWS Lambda
Because data received from Opensky-Api contain data about all airplanes in specified geographic bounding box, then these contains data about airplanes above Poland, and some of neighboring countries. AWS Lambda is then used in order to remove data about airplanes that aren't above Poland. On the end of AWS Lambda function, the most important data are saved into AWS DynamoDB tables.


### AWS DynamoDB
AWS DynamoDB is used as storage for historical and last data of airplanes above Poland in two tables.

* Table for historical data has primary key which is ICAO24 of airplane and sort key which is timestamp of sending request to Opensky-API

* Table for last data has only primary key which is ICAO24. Lack of sort key enable to overwrite data for each airplane

Each table contain following columns:
* ICAO24
* timestamp
* datetime
* latitude
* longitude
* heading
* velocity


### Local Machine
Local Machine (that is personal computer) is used to repeatedly reading data from DynamoDB table with last airplanes data and visualize them with use of Mapbox.


### Exemplary view on airplanes above Poland
![diagram](https://github.com/jwszol-classes/isp-2020-ZekJakGynDam/blob/simple_visualization/src/final_view_simple.png)

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


#### Instance setup - configure git
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
* download repository
```
git clone git@github.com:jwszol-classes/isp-2020-ZekJakGynDam.git
cd isp-2020-ZekJakGynDam/
```
* setup repository
```
source ./ec2_setup.sh
```

#### Instance setup - configure AWS
* open labs.vocareum page
* click **Account Details**
* click **show**
* copy showed text
* paste it into ~/.aws/credentials


#### Instance setup - create image
* go to EC2 service
* click **Instances (running)**
* click right mouse button on instance
* choose **Image and templates**
* choose **Create image**
* provide **Image name** (for example "image_airplanes")
* uncheck **Delete on termination** checkbox
* click **Create image**
* go to EC2 service
* go to Images/AMIs
* wait until **Status** of your image change into "available" (don't terminate instance until then!!!)



### Prepare AWS Services

#### Kinesis, S3, Lambda, DynamoDB
* go to ~/Projects/isp-2020-ZekJakGynDam/ on EC2 instance
* Prepare aws_services_config.json file in main project directory by aws_services_config_default.json and changing each "XxXxxXXxxXxX" into your AWS user id (12 digits) (don't add this file to repository!). You can also change names of each AWS services elements in this file.
* run following command:
```
python aws_services_creator.py
```

#### Adding Trigger to Lambda function
* go to **Lambda** service page
* choose "lambda_function_airplanes" function
* click **Add trigger**
* select a **trigger** ("Kinesis")
* choose **Kinesis stream** ("kinesis_data_stream_airplanes")
* click **Add**



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
python kinesis\producer.py
```
On local machine run to visualization airplanes:
```
python visualisation_animation_plotly.py
```
Open following url link in browser:
```
http://127.0.0.1:8050/
```
