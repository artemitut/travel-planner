# Travel Planner API

RESTful API for managing travel projects and places to visit.

---

## Features

- Create and manage travel projects
- Add places to projects (from external API)
- Attach notes to places
- Mark places as visited
- Automatically complete project when all places are visited
- Validate places using Art Institute of Chicago API

---

## Tech Stack

- Python 3
- Flask
- SQLAlchemy
- SQLite
- Requests

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/artemitut/travel-planner
cd travel-planner
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python run.py
```

---

## API Endpoints

### Projects

- `POST /projects/` - Create a project
- `GET /projects/` - Get all projects
- `GET /projects/{id}` - Get project by ID
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### Places

- `POST /places/{project_id}` - Add a place to a project
- `GET /places/{project_id}` - Get all places in a project
- `GET /places/{project_id}/{place_id}` - Get a single place
- `PUT /places/{project_id}/{place_id}` - Update a place

---

## External API

This project uses the [Art Institute of Chicago API](https://api.artic.edu/docs/) to:

- Validate places
- Fetch place titles

---

## Business Rules

- Maximum 10 places per project
- Cannot add duplicate places (same `external_id`)
- Place must exist in the external API
- Cannot delete a project if any place is marked as visited
- Project is marked as completed when all places are visited

---

## Postman Collection

You can test all endpoints using Postman.  

Import the collection from the repository: `postman_collection.json`