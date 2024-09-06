from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_team = db.Table('user_team',
    db.Column('user_id', db.String(80), db.ForeignKey('user.id'), primary_key=True),
    db.Column('team_id', db.String(80), db.ForeignKey('team.id'), primary_key=True)
)

user_schedule = db.Table('user_schedule',
    db.Column('user_id', db.String(80), db.ForeignKey('user.id'), primary_key=True),
    db.Column('schedule_id', db.String(80), db.ForeignKey('schedule.id'), primary_key=True)
)

class Team(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    service_id = db.Column(db.String(80), db.ForeignKey('service.id'), nullable=True)
    users = db.relationship('User', secondary=user_team, backref=db.backref('teams', lazy=True))

class Schedule(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    time_zone = db.Column(db.String(200), nullable=False)
    users = db.relationship('User', secondary=user_schedule, backref=db.backref('schedules', lazy=True))

class Service(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(200), nullable=False)
    teams = db.relationship('Team', backref='team', lazy=True)
    incidents = db.relationship('Incident', backref='incident', lazy=True)
    escalation_policy_id = db.Column(db.String(80), db.ForeignKey('escalation_policy.id'), nullable=True)

class User(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class Incident(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(120), nullable=False)
    service_id = db.Column(db.String(80), db.ForeignKey('service.id'))

class EscalationPolicy(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    services = db.relationship('Service', backref='service', lazy=True)



