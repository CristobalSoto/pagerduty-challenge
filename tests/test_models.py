# tests/test_models.py
import pytest
from config import TestingConfig
from app import create_app
from app.models import db, User, Team, Service, Incident

def test_user_creation(test_client):
    user = User(id="123", name="John Doe", email="john@example.com")
    db.session.add(user)
    db.session.commit()

    fetched_user = User.query.get("123")
    assert fetched_user.name == "John Doe"
    assert fetched_user.email == "john@example.com"

def test_team_creation(test_client):
    team = Team(id="456", name="DevOps", service_id=None)
    db.session.add(team)
    db.session.commit()

    fetched_team = Team.query.get("456")
    assert fetched_team.name == "DevOps"
    assert fetched_team.service_id is None

def test_service_creation(test_client):
    service = Service(id="789", name="PagerDuty", description="Incident management service", status="active")
    db.session.add(service)
    db.session.commit()

    fetched_service = Service.query.get("789")
    assert fetched_service.name == "PagerDuty"
    assert fetched_service.description == "Incident management service"
    assert fetched_service.status == "active"

def test_user_team_relationship(test_client):
    # Create a unique team and user
    team = Team(id="team-123", name="DevOps", service_id=None)
    user = User(id="user-123", name="John Doe", email="john@example.com")
    db.session.add(team)
    db.session.add(user)
    db.session.commit()

    # Assign user to the team via the user_team association
    user.teams.append(team)
    db.session.commit()

    # Verify the relationship
    fetched_user = User.query.get("user-123")
    assert len(fetched_user.teams) == 1
    assert fetched_user.teams[0].name == "DevOps"

    # Clean up
    db.session.delete(fetched_user)
    db.session.delete(team)
    db.session.commit()

def test_service_team_relationship(test_client):
    # Create a unique service and team
    service = Service(id="service-123", name="PagerDuty", status="active")
    team = Team(id="team-456", name="DevOps", service_id=service.id)
    db.session.add(service)
    db.session.add(team)
    db.session.commit()

    # Verify the relationship between service and team
    fetched_service = Service.query.get("service-123")
    assert len(fetched_service.teams) == 1
    assert fetched_service.teams[0].name == "DevOps"

    # Clean up
    db.session.delete(fetched_service)
    db.session.delete(team)
    db.session.commit()

def test_service_incident_relationship(test_client):
    # Create a unique service and incident
    service = Service(id="service-789", name="PagerDuty", status="active")
    incident = Incident(id="incident-001", title="Outage", description="System outage", status="open", service_id=service.id)
    db.session.add(service)
    db.session.add(incident)
    db.session.commit()

    # Verify the relationship between service and incident
    fetched_service = Service.query.get("service-789")
    assert len(fetched_service.incidents) == 1
    assert fetched_service.incidents[0].title == "Outage"

    # Clean up
    db.session.delete(fetched_service)
    db.session.delete(incident)
    db.session.commit()