# Q&A Forum Backend with FastAPI
FastAPI + PostgreSQL backend for a Q&amp;A platform
# Q&A Backend API (FastAPI + PostgreSQL)

A simple backend API for a Q&A platform (similar to StackOverflow).  
This project connects to an **existing PostgreSQL database** (tables + PL/pgSQL functions already created) and exposes REST endpoints using **FastAPI**.

## Related SQL Project (Database)
This backend is built on top of my SQL project repo (schema + data + functions):

- **Q-A-Platform-SQL**: https://github.com/Aram-Atoyan/Q-A-Platform-SQL

---

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy (DB connection + executing SQL)

---

## How this relates to the SQL project
- The SQL repo contains:
  - database schema (**DDL**)
  - sample data (**DML**)
  - stored functions for operations (**PL/pgSQL**)
  - reporting queries
- This backend repo:
  - connects to that database
  - calls those stored functions from API endpoints

---

## What this API does
The API calls existing database functions to:
- register users
- create questions
- create answers
- add comments
- vote on questions or answers
- list users and questions

---

## Project files
- `main.py` — FastAPI app + router setup
- `routes.py` — API endpoints (calls DB functions / queries)
- `db.py` — PostgreSQL connection + session dependency
- `reset_sequences.sql` (optional) — fixes ID sequences if seed data was inserted manually

---

## Setup

### 1) Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 2) Install Dependencies
```bash
pip install -r requirements.txt
```
### 3) Prepare the database
Before running this API, set up the database using the SQL repo provided at the start of the file:

Run in this order (from the SQL repo):
	1.	`DDL.sql`
	2.	`DML.sql`
	3.	`DQL_Data_Operations.sql`
	4.	`DQL_DataReporting.sql`

### 4) Configure database connection
Edit `db.py` and set your PostgreSQL connection string:
```python
DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@localhost:PORT/DBNAME"
```

### 5) Start the server
```bash
uvicorn main:app --reload
```
Open Swagger docs:
	•	http://127.0.0.1:8000/docs


