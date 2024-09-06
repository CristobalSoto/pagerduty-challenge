## Introduction

This README outlines the steps required to set up and run this project on a local machine. It provides a systematic approach to ensure the project is correctly configured for development and execution.

## Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

## Setup Instruction with Docker-compose

```bash
docker-compose down
docker-compose up --build
```


## Setup Instructions To run the project without docker

### Step 1: Create a Virtual Environment

To isolate and manage dependencies, create a virtual environment in your project directory:
python -m venv venv

### Step 2: Activate the Virtual Environment

Activate the virtual environment with the following command:

On Windows:

```cmd
.\venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment activated, install the required dependencies:

```python
pip install -r requirements.txt
```

### Step 4: Create database

Run the creation of the database (this will create the tables)

```python
python seed_data.py
```


### Step 5: Run the Project

Finally, run the project from the root directory:

```python
python run.py
```
### Run test:

```bash
pytest
```


## Endpoints

### 1. Home
- **URL**: `/`
- **Method**: `GET`
- **Description**: Displays a home message for the PagerDuty Dashboard API.

### 2. Import Data from PagerDuty
- **URL**: `/import-data`
- **Method**: `POST`
- **Description**: Imports data from PagerDuty and stores it in the database.

### 3. Get JSON Report
- **URL**: `/reports`
- **Method**: `GET`
- **Description**: Retrieves a report in JSON format with data from PagerDuty.

### 4. Download CSV Report
- **URL**: `/reports/csv`
- **Method**: `GET`
- **Description**: Downloads a CSV file of the report generated from PagerDuty data.

### 5. Get Service Incident Analysis
- **URL**: `/reports/analysis`
- **Method**: `GET`
- **Description**: Provides an analysis of the service with the most incidents.

### 6. Get Incident Analysis Graph
- **URL**: `/reports/analysis/graph`
- **Method**: `GET`
- **Description**: Generates and returns a graph showing the breakdown of incidents by status for the service with the most incidents.

### 7. Get Inactive Users
- **URL**: `/reports/inactive-users`
- **Method**: `GET`
- **Description**: Retrieves a list of inactive users from the PagerDuty data.

### 7. Get Inactive Users
- **URL**: `/incidents-batch`
- **Method**: `POST`
- **Description**: Inserts Incidents in to the PagerDuty Database.
