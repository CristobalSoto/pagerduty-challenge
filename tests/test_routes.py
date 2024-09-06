import pytest
from unittest.mock import patch, AsyncMock
from flask import Flask


def test_get_csv_report(test_client):
    csv_mock_data = "\n\nservices_count\nservices_count\n0\n\n\nincidents_per_service\n\n\nincidents_by_service_and_status\n\n\nteams_and_services\n\n\n"
    
    with patch('app.services.report_service.generate_csv', AsyncMock(return_value=csv_mock_data)):
        response = test_client.get('/reports/csv')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'services_count' in response.data  # Asserting expected part of the CSV

def test_get_analysis(test_client):
    with patch('app.routes.analyze_service_with_most_incidents', return_value={
        "service_name": "Service A", "incident_count": 10
    }) as mock_analyze:
        response = test_client.get('/reports/analysis')
        assert response.status_code == 200
        data = response.get_json()
        
        # Check if the mock was called
        mock_analyze.assert_called_once()

        # Check for the correct values in the response
        assert "service_name" in data
        assert data["service_name"] == "Service A"
        assert data["incident_count"] == 10

def test_get_analysis_graph(test_client):
    with patch('app.routes.analyze_service_with_most_incidents', return_value={
        "service_with_most_incidents": "ServiceA",
        "incident_breakdown_by_status": [{"status": "open", "count": 10}]
    }), patch('matplotlib.pyplot.savefig'):
        response = test_client.get('/reports/analysis/graph')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'image/png'

def test_get_inactive_users(test_client):
    with patch('app.routes.analyze_inactive_users', return_value=[{"user": "UserA", "status": "inactive"}]):
        response = test_client.get('/reports/inactive-users')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0  # Ensure the list has at least one element
        assert data[0]["user"] == "UserA"
        assert data[0]["status"] == "inactive"

