import json
from app.batch_processing import IncidentBatchProcessor
from app.commands import CreateIncidentCommand
import os
from app.constants import API_KEY, BASE_URL

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
incidents_file_path = os.path.join(root_dir, 'data', 'incidents.json')


def add_incidents_in_pagerduty():
    url = f'{BASE_URL}/incidents'
    headers = {
        "Authorization": f"Token token={API_KEY}",
        "From": "mariana@pagerduty.com",
        "Content-Type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }

    with open(incidents_file_path) as json_file:
        incidents = json.load(json_file)

    batch_processor = IncidentBatchProcessor()

    # Add a command for each incident
    for incident in incidents:
        command = CreateIncidentCommand(incident, url, headers)
        batch_processor.add_command(command)

    # Execute all the commands
    batch_processor.execute_all()
