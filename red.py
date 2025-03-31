import requests
from requests.auth import HTTPBasicAuth

# Reddit API credentials
client_id = '8FUxHW8uydtAt9H34Os27g'
client_secret = '3MxM_FITAvW3y7ZXqJZDgYPn9o5oUg'
username = 'NoMoreTeen'
password = 'Rit@reddit'

# Reddit API URL
url = 'https://www.reddit.com/api/v1/access_token'

# Prepare the authentication
auth = HTTPBasicAuth(client_id, client_secret)

# Prepare the payload for the request
data = {
    'grant_type': 'password',
    'username': username,
    'password': password,
}

# Make the POST request to get the access token
response = requests.post(url, data=data, auth=auth)

# Get the access token from the response
access_token = response.json()['access_token']
