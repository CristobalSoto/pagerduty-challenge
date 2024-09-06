import json
import requests


class IncidentCommand:
    def execute(self):
        raise NotImplementedError

class CreateIncidentCommand(IncidentCommand):
    def __init__(self, incident_data, url, headers):
        self.incident_data = incident_data
        self.url = url
        self.headers = headers

    def execute(self):
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.incident_data))
        if response.status_code == 201:
            print(f"Incident created successfully: {response.status_code}")
        else:
            print(f"Failed to create incident: {response.status_code}, {response.text}")
