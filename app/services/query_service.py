from flask import jsonify
from sqlalchemy import func, not_
from sqlalchemy.orm import aliased
from app.models import Service, Incident, User, db  # Make sure your database instance is imported

def analyze_service_with_most_incidents():
    # Query for incidents per service
    incidents_per_service = db.session.query(
        Service.name, func.count(Incident.id)
    ).join(Incident).group_by(Service.id).all()
    
    if not incidents_per_service:
        return {"service_name": None, "incident_count": 0}

    # Find the service with the most incidents
    service_with_most_incidents = max(incidents_per_service, key=lambda x: x[1])

    # Query for incident breakdown by status for the service with the most incidents
    incident_breakdown_by_status = db.session.query(
        Incident.status, func.count(Incident.id)
    ).filter(Incident.service_id == Service.id).group_by(Incident.status).all()

    # Return the analysis results
    return {
        "service_with_most_incidents": service_with_most_incidents[0],
        "total_incidents": service_with_most_incidents[1],
        "incident_breakdown_by_status": [{"status": row[0], "count": row[1]} for row in incident_breakdown_by_status]
    }
def analyze_inactive_users():
    # Fetch all users and check if their schedules are empty
    inactive_users = db.session.query(User).all()

    # Filter for users with no schedules
    inactive_users = [user for user in inactive_users if not user.schedules]

    # Convert the result into a list of dictionaries
    return [{"user_name": user.name, "email":user.email, "schedules": user.schedules} for user in inactive_users]