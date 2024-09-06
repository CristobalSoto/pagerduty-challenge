from app.models import EscalationPolicy, Service, Incident, Team, db
from sqlalchemy import func

class ServiceRepository:
    def __init__(self, session):
        self.session = session

    def get_services_count(self):
        return self.session.query(func.count(Service.id)).scalar()

    def get_incidents_per_service(self):
        results = self.session.query(Service.name, func.count(Incident.id))\
                         .join(Incident)\
                         .group_by(Service.id).all()
        return [{"service_name": row[0], "incident_count": row[1]} for row in results]

    def get_incidents_by_service_and_status(self):
        results = self.session.query(Service.name, Incident.status, func.count(Incident.id))\
                         .join(Incident)\
                         .group_by(Service.id, Incident.status).all()
        return [{"service_name": row[0], "status": row[1], "incident_count": row[2]} for row in results]

class TeamRepository:
    def __init__(self, session):
        self.session = session

    def get_teams_and_services(self):
        results = self.session.query(Team.name, func.count(Service.id))\
                         .join(Service)\
                         .group_by(Team.id).all()
        return [{"team_name": row[0], "service_count": row[1]} for row in results]

class EscalationRepository:
    
    def __init__(self, session):
        self.session = session
    def get_escalation_policies_with_teams_and_services(self):
        results = db.session.query(
            EscalationPolicy.name.label('escalation_policy_name'),  
            Service.name.label('service_name'),  
            Team.name.label('team_name')
        ).join(Service, EscalationPolicy.services).join(Team, Team.service_id == Service.id).all()

        return [{"escalation_policy_name": row[0], "service_name": row[1], "team_name": row[2]} for row in results]
