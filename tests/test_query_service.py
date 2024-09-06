# Let's define unit tests for the query functions in 'query_service.py'
import pytest
from unittest.mock import patch
from app.services.query_service import (
    analyze_service_with_most_incidents,
)


@patch('app.services.query_service.db.session.query')
def test_analyze_service_with_most_incidents_no_data(mock_query):
    # Mock the query to return an empty list for the incidents per service
    mock_query.return_value.join.return_value.group_by.return_value.all.return_value = []

    # Call the function
    result = analyze_service_with_most_incidents()

    # Assert the result is None for the service and 0 for incidents
    assert result == {"service_name": None, "incident_count": 0}




