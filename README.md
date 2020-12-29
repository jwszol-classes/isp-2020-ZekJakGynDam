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

##### Linux

#### Kinesis


#### AWS Lambda
##### Creating Lambda Function 
* Go under following URL link https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions
* click **Create function**
* choose **Author from scratch**
* provide **Function name** (for example "lambda_airplanes")
* provide Runtime (**Python 3.8**)
* expand **Change default execution role** and remember execution role name assigned to lambda function (for example "lambda_airplanes-role-p5nao7pr")
* click **Create function**

##### Adding layer with numpy and scipy modules
* click **Layers** and choose **Add a layer**
* choose **AWS layers** ("AWSLambda-Python38-SciPy1x") and **Version** ("29")
* click **Add**

##### Adding Trigger
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

##### Adding resources
* go to isp-2020-ZekJakGynDam\aws_lambda directory
* zip lambda_function_airplanes.py and reverse_geocode directory into .zip archive (for example "aws_lambda.zip")
* in lambda function page click on **lambda_airplanes**
* Under **Function code** section click **Actions**
* choose **Upload a .zip file**
* find and save "aws_lambda.zip"
* go under **Runtime settings** settings and click **Edit**
* change Handler into "lambda_function_airplanes.lambda_handler_airplanes"
* click **Save**

##### Congratulations
You have just configured AWS Lambda function for checking if airplane is above Poland and updating DynamoDB tables! Congratulations.

#### Credentials
Prepare credentials.json file in main project directory by duplicate credentials_default.json and changing its name (don't add this file to repository!). Fill places with your registrations and api keys data




#### AWS


#### Communication
* PuTTy
* Xming


### Run
```
python opensky_test.py
python geoapify_test.py
python visualisation.py
```
