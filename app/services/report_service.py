import pandas as pd
from app.repositories import EscalationRepository, ServiceRepository, TeamRepository
from app.models import db

session = db.session 
service_repo = ServiceRepository(session)
team_repo = TeamRepository(session)
escalation_repo = EscalationRepository(session)

# Refactor to use repositories instead of direct queries
async def gather_report_data(for_csv):
    if for_csv:
        services_count = pd.DataFrame([{"services_count": service_repo.get_services_count()}])
        incidents_per_service = pd.DataFrame(service_repo.get_incidents_per_service())
        incidents_by_service_and_status = pd.DataFrame(service_repo.get_incidents_by_service_and_status())
        teams_and_services = pd.DataFrame(team_repo.get_teams_and_services())
        escalation_policies_teams_services = pd.DataFrame(escalation_repo.get_escalation_policies_with_teams_and_services())
    else:
        services_count = service_repo.get_services_count()
        incidents_per_service = service_repo.get_incidents_per_service()
        incidents_by_service_and_status = service_repo.get_incidents_by_service_and_status()
        teams_and_services = team_repo.get_teams_and_services()
        escalation_policies_teams_services = escalation_repo.get_escalation_policies_with_teams_and_services()

    return {
        "services_count": services_count,
        "incidents_per_service": incidents_per_service,
        "incidents_by_service_and_status": incidents_by_service_and_status,
        "teams_and_services": teams_and_services, 
        "escalation_policies_teams_services": escalation_policies_teams_services
    }

def convert_to_csv(report_dataframes):
    csv_data = []
    for name, df in report_dataframes.items():
        csv_data.append(f"\n\n{name}\n")
        csv_data.append(df.to_csv(index=False))
    return ''.join(csv_data)

# Main function using repositories
async def generate_csv():
    report_dataframes = await gather_report_data(True)
    return convert_to_csv(report_dataframes)
