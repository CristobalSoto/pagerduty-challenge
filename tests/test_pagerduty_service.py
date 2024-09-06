# Let's define tests for the functions in 'pagerduty_service.py'
import pytest
from unittest.mock import patch, AsyncMock
from app.models import Team, Service, db
from app.services.pagerduty_service import fetch_pagerduty_data, store_teams, store_services

# Test for fetch_pagerduty_data
@pytest.mark.asyncio
@patch('app.services.pagerduty_service.aiohttp.ClientSession.get')
async def test_fetch_pagerduty_data(mock_get):
    # Mock the response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"data": "some_data"}
    mock_get.return_value.__aenter__.return_value = mock_response
    
    # Call the function
    data = await fetch_pagerduty_data('some-endpoint')
    
    # Assert the data is correctly returned
    assert data == {"data": "some_data"}
    mock_get.assert_called_once()

@pytest.mark.asyncio
@patch('app.services.pagerduty_service.fetch_pagerduty_data', new_callable=AsyncMock)
async def test_store_teams(mock_fetch_data, test_client):
    # Mock the fetch_pagerduty_data to return sample team data
    mock_fetch_data.return_value = {
        "teams": [
            {"id": "team-123", "name": "DevOps Team"},
            {"id": "team-456", "name": "Ops Team"}
        ]
    }
    
    # Call the store_teams function
    await store_teams()

    # Verify teams are stored in the database
    teams = Team.query.all()
    assert len(teams) == 2
    assert teams[0].name == "DevOps Team"
    assert teams[1].name == "Ops Team"

@pytest.mark.asyncio
@patch('app.services.pagerduty_service.fetch_pagerduty_data', new_callable=AsyncMock)
async def test_store_services(mock_fetch_data, test_client):
    # Mock the fetch_pagerduty_data to return sample service data
    mock_fetch_data.return_value = {
        "services": [
            {
                "id": "service-123",
                "name": "Incident Management",
                "description": None,
                "status": "active",
                "teams": [
                    {
                      'id':"team-123"
                    }
                ]
            }
        ]
    }

    # Call the store_services function
    await store_services()

    # Verify services and team-service relationships are stored in the database
    service = Service.query.get("service-123")
    assert service.name == "Incident Management"
    assert service.description == "No description provided"
    assert service.status == "active"
    
    # Verify the team relationship
    team = Team.query.get("team-123")
    assert team is not None
    assert team.service_id == "service-123"