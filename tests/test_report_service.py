import pytest
from unittest.mock import AsyncMock, patch
import pandas as pd
from app.services import report_service


@pytest.mark.asyncio
async def test_gather_report_data_csv(test_client):
    # Mock repository methods
    with patch('app.repositories.ServiceRepository.get_services_count', return_value=5), \
         patch('app.repositories.ServiceRepository.get_incidents_per_service', return_value=[{"service": "ServiceA", "incidents": 10}]), \
         patch('app.repositories.ServiceRepository.get_incidents_by_service_and_status', return_value=[{"service": "ServiceA", "status": "open", "count": 5}]), \
         patch('app.repositories.TeamRepository.get_teams_and_services', return_value=[{"team": "TeamA", "service": "ServiceA"}]), \
         patch('app.repositories.EscalationRepository.get_escalation_policies_with_teams_and_services', return_value=[{"team": "TeamA", "policy": "PolicyA"}]):

        # Call the function
        result = await report_service.gather_report_data(for_csv=True)

        # Assert the result is a dictionary with expected dataframes
        assert isinstance(result['services_count'], pd.DataFrame)
        assert isinstance(result['incidents_per_service'], pd.DataFrame)
        assert isinstance(result['incidents_by_service_and_status'], pd.DataFrame)
        assert isinstance(result['teams_and_services'], pd.DataFrame)
        assert isinstance(result['escalation_policies_teams_services'], pd.DataFrame)


@pytest.mark.asyncio
async def test_gather_report_data_non_csv(test_client):
    # Mock repository methods
    with patch('app.repositories.ServiceRepository.get_services_count', return_value=5), \
         patch('app.repositories.ServiceRepository.get_incidents_per_service', return_value=[{"service": "ServiceA", "incidents": 10}]), \
         patch('app.repositories.ServiceRepository.get_incidents_by_service_and_status', return_value=[{"service": "ServiceA", "status": "open", "count": 5}]), \
         patch('app.repositories.TeamRepository.get_teams_and_services', return_value=[{"team": "TeamA", "service": "ServiceA"}]), \
         patch('app.repositories.EscalationRepository.get_escalation_policies_with_teams_and_services', return_value=[{"team": "TeamA", "policy": "PolicyA"}]):

        # Call the function
        result = await report_service.gather_report_data(for_csv=False)

        # Assert the result is a dictionary with expected raw data (not DataFrames)
        assert isinstance(result['services_count'], int)
        assert isinstance(result['incidents_per_service'], list)
        assert isinstance(result['incidents_by_service_and_status'], list)
        assert isinstance(result['teams_and_services'], list)
        assert isinstance(result['escalation_policies_teams_services'], list)


def test_convert_to_csv(test_client):
    # Create sample dataframes
    data = {
        "services_count": pd.DataFrame([{"service_count": 5}]),
        "incidents_per_service": pd.DataFrame([{"service": "ServiceA", "incidents": 10}])
    }
    
    # Call the function
    csv_result = report_service.convert_to_csv(data)
    
    # Assert CSV content
    assert "services_count" in csv_result
    assert "service_count" in csv_result
    assert "ServiceA" in csv_result


@pytest.mark.asyncio
async def test_generate_csv(test_client):
    # Mock internal functions
    with patch('app.services.report_service.gather_report_data', AsyncMock(return_value={
        "services_count": pd.DataFrame([{"service_count": 5}]),
        "incidents_per_service": pd.DataFrame([{"service": "ServiceA", "incidents": 10}])
    })), \
    patch('app.services.report_service.convert_to_csv', return_value="CSV_CONTENT"):
        
        # Call the function
        csv_content = await report_service.generate_csv()
        
        # Assert the CSV content
        assert csv_content == "CSV_CONTENT"
