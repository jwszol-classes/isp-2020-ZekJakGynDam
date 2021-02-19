import requests
import json
from bs4 import BeautifulSoup


def extract_aws_credentials(page_text):
    soup = BeautifulSoup(page_text, 'html.parser')
    pres = soup.find_all('pre')
    print(pres)
    aws_credentials = pres[0].text
    return aws_credentials


def get_actual_aws_credentials(vocareum_dict):
    url_refresh         = "https://labs.vocareum.com/main/main.php?m=editor&nav=1&asnid=305143&stepid=305144"
    url_aws_credentials = "https://labs.vocareum.com/util/vcput.php?a=getaws&nores=1&stepid=305144&version=0&mode=s&type=0"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50'}
    
    cookies = vocareum_dict["cookies"]

    p = requests.get(url_refresh,         cookies=cookies, headers=headers)
    p = requests.get(url_aws_credentials, cookies=cookies, headers=headers)
    aws_credentials = extract_aws_credentials(p.text)
    return aws_credentials


def save_aws_credentials(aws_dict, aws_credentials):
    file_aws_credentials = open(aws_dict["credentials_path"], "w")
    file_aws_credentials.write(aws_credentials)
    file_aws_credentials.close()


def get_and_save_actual_aws_credentials(credentials):
    aws_dict      = credentials["aws"]
    vocareum_dict = credentials["vocareum"]
    aws_credentials = get_actual_aws_credentials(vocareum_dict)
    save_aws_credentials(aws_dict, aws_credentials)


if __name__ == "__main__":
    credentials_path = "credentials.json"
    credentials = json.load(open(credentials_path, "r"))
    aws_credentials = get_and_save_actual_aws_credentials(credentials)
