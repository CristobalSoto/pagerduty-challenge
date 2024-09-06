import requests
import json

# The URL and Authorization header for PagerDuty
url = "https://api.pagerduty.com/incidents"
headers = {
    "Authorization": "Token token=u+b4CCjDZsXfuxx-w_fw",
    "From": "mariana@pagerduty.com",
    "Content-Type": "application/json",
    "Accept": "application/vnd.pagerduty+json;version=2"
}

with open('incidents.json') as json_file:
    incidents = json.load(json_file)

# Loop over incidents and submit each one
for incident in incidents:
    response = requests.post(url, headers=headers, data=json.dumps(incident))
    
    if response.status_code == 201:
        print(f"Incident created successfully: {response.status_code}")
    else:
        print(f"Failed to create incident: {response.status_code}, {response.text}")