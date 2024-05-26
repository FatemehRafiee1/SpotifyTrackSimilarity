import os
import requests
import base64

from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('Client_ID')
client_secret = os.getenv('Client_secret')

# Encode client ID and client secret
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode('utf-8'))
# Get the token
token_url = "https://accounts.spotify.com/api/token"
token_data = {
    "grant_type": "client_credentials"
}
token_headers = {
    "Authorization": f"Basic {str(client_creds_b64, 'utf-8')}",
    "Content-Type": "application/x-www-form-urlencoded"
}

r = requests.post(token_url, data=token_data, headers=token_headers)
token_response_data = r.json()
access_token = token_response_data['access_token']

print("acc: ", access_token)