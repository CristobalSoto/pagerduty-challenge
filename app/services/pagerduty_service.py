from app.models import EscalationPolicy, Incident, Schedule, User, db, Service, Team
import aiohttp
from constants import API_KEY, BASE_URL


async def fetch_pagerduty_data(endpoint: str) -> dict:
    url = f'{BASE_URL}/{endpoint}'
    headers = {
        'Authorization': f'Token token={API_KEY}',
        'Accept': 'application/vnd.pagerduty+json;version=2'
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()  # Raises an exception for bad status
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f'Other error occurred: {e}')
        return None

async def store_teams() -> None:
    teams_data = await fetch_pagerduty_data('teams')  # Use await for the async fetch
    if teams_data and 'teams' in teams_data:
        teams = [Team(id=item['id'], name=item['name']) for item in teams_data['teams']]
        
        # Asynchronous database operations (SQLAlchemy does not support async natively, so commit is synchronous)
        db.session.bulk_save_objects(teams)
        db.session.commit()


async def store_services():
    services_data = await fetch_pagerduty_data('services')
    team_updates = []  # To store team-service relationships

    for item in services_data['services']:
        if item['description'] is None:
            description = 'No description provided'
        else:
            description = item['description']
        
        service = Service(id=item['id'], name=item['name'], description=description, status=item['status'])
        db.session.add(service)

        # Handle team-service relationships
        for team_id in item['teams']:
            team = Team.query.filter_by(id=team_id['id']).first()
            if team:
                # Update the service_id of the team
                team.service_id = item['id']
                team_updates.append(team)

    db.session.add_all(team_updates)
    db.session.commit()

async def store_incidents():
    incidents_data = await fetch_pagerduty_data('incidents')
    incidents = []
    for item in incidents_data['incidents']:
        if 'service' in item and 'id' in item['service']:  # Ensure service info is present
            incident = Incident(
                id=item['id'],
                title=item.get('title', 'No Title Provided'),
                description=item.get('description', 'No Description Provided'),
                status=item['status'],
                service_id=item['service']['id']
            )
            incidents.append(incident)
        else:
            print(f"Missing service details for incident {item['id']}")

    db.session.bulk_save_objects(incidents)
    db.session.commit()



async def store_users():
    users_data = await fetch_pagerduty_data('users')

    for item in users_data.get('users', []):
        user = User(id=item['id'], name=item['name'], email=item['email'])

        # Assume that user-team relationships are provided within each user item
        for team_id in item.get('teams', []):
            team = Team.query.filter_by(id=team_id['id']).first()
            team.users.append(user)

    db.session.commit()


async def store_escalation_policies():
    escalation_data = await fetch_pagerduty_data('escalation_policies')
    services_updates = []

    for item in escalation_data.get('escalation_policies', []):
        policy = EscalationPolicy(
            id=item['id'],
            name=item['name'],
        )
        db.session.add(policy) # save the service to update the teams table with service id
        for service_obj in item['services']:
            service = Service.query.filter_by(id=service_obj['id']).first()
            if service:
                # Update the service_id of the team
                service.escalation_policy_id = item['id']
                services_updates.append(service)

    db.session.bulk_save_objects(services_updates)
    db.session.commit()

async def store_schedules():
    schedules_data = await fetch_pagerduty_data('schedules')
    schedules = []

    for item in schedules_data.get('schedules', []):
        schedule = Schedule(
            id=item['id'],
            name=item['name'],
            time_zone=item['time_zone']
        )
        
        db.session.add(schedule)
        
        for user_obj in item.get('users', []):
            user = User.query.filter_by(id=user_obj['id']).first()
            if user:  # Only append if user is found
                schedule.users.append(user)

        schedules.append(schedule)


    db.session.bulk_save_objects(schedules)
    db.session.commit()

