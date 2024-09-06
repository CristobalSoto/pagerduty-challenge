import os
from flask import jsonify, make_response
from app.services.query_service import analyze_inactive_users, analyze_service_with_most_incidents
from app.services.report_service import gather_report_data, generate_csv
from app.repositories import EscalationRepository, ServiceRepository, TeamRepository
from app.services.insert_incidents_service import add_incidents_in_pagerduty
from .services.pagerduty_service import store_escalation_policies, store_incidents, store_schedules, store_services, store_teams, store_users
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
from flask import send_file
import asyncio


def configure_routes(app):
    @app.route('/')
    def home():
        return 'PagerDuty Dashboard API Home'

    # POST route for importing data from PagerDuty
    @app.route('/import-data', methods=['POST'])
    def fetch_store_data():
        asyncio.run(store_teams())
        asyncio.run(store_services())
        asyncio.run(store_incidents())
        asyncio.run(store_users())
        asyncio.run(store_escalation_policies())
        asyncio.run(store_schedules())
        return jsonify({"message": "Data fetched and stored successfully"}), 201

    @app.route('/incidents-batch', methods=['POST'])
    def send_incidents_to_pagerduty():
        add_incidents_in_pagerduty()
        return jsonify({"message": "Incidents inserted successfully"}), 201

    # GET route for fetching a JSON report
    @app.route('/reports', methods=['GET'])
    def get_report():
        report = asyncio.run(gather_report_data(False))
        return jsonify(report), 200

    # GET route for downloading a CSV report
    @app.route('/reports/csv', methods=['GET'])
    def get_csv_report():
        try:
            csv_data = asyncio.run(generate_csv())
            # Create a Flask response to download the CSV
            response = make_response(csv_data)
            response.headers["Content-Disposition"] = "attachment; filename=report.csv"
            response.headers["Content-Type"] = "text/csv"
            return response, 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # GET route for generating analysis
    @app.route('/reports/analysis', methods=['GET'])
    def get_analysis():
        analysis = analyze_service_with_most_incidents()
        return jsonify(analysis), 200

    # GET route for generating an analysis graph
    @app.route('/reports/analysis/graph', methods=['GET'])
    def get_analysis_graph():
        analysis = analyze_service_with_most_incidents()

        # Data for the graph
        statuses = [entry['status'] for entry in analysis['incident_breakdown_by_status']]
        counts = [entry['count'] for entry in analysis['incident_breakdown_by_status']]

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.bar(statuses, counts, color='skyblue')
        plt.title(f"Incident Breakdown by Status for {analysis['service_with_most_incidents']}")
        plt.xlabel('Incident Status')
        plt.ylabel('Number of Incidents')

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Return the image as a response
        return send_file(img, mimetype='image/png'), 200

    # GET route for retrieving inactive users
    @app.route('/reports/inactive-users', methods=['GET'])
    def get_inactive_users():
        inactive_users = analyze_inactive_users()
        return jsonify(inactive_users), 200
