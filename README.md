# 🌍 Countries API (v1 / Beta)

A RESTful API containing data for **192 countries** from around the world. This project serves as an early-stage (**v1 / beta**) foundation for a more complete and structured global data platform. While the current implementation is functional, it is **not fully optimized or well organized**, and many improvements and features are planned for future versions.

---

## 📌 Overview

The Countries API provides structured data across multiple domains, including:

- Countries  
- Regions  
- Languages  
- Cities  
- Development indicators  
- Economic data  

The goal of this project is to centralize country-level information in a way that is easy to query, extend, and integrate into other applications.

---

## ✨ Features

### 🔍 Smart Filter Search
Search using **related keywords or phrases** to locate relevant country data without relying on exact matches.

### 📊 Country Comparison
Compare statistics for **up to 4 countries on a single screen**, allowing for quick side-by-side analysis of development and economic indicators.

### 🧠 Relational Data Model
Data is structured using relational models, linking countries to regions, languages, development metrics, and economic information.

---

**Quick start**
Activate the project venv:

source .venv/bin/activate

Install dependencies (if you don't already have them):

# if you have a requirements.txt
pip install -r requirements.txt

# or install core deps manually
pip install Flask Flask-SQLAlchemy Flask-Migrate flask-cors pandas gunicorn

Run DB migrations and seed data:

export FLASK_APP=app.py
export FLASK_ENV=development
flask db upgrade
python seed_database.py

Start the backend (example using gunicorn):

gunicorn --bind 127.0.0.1:8000 "app:create_app()" --workers 3

Serve the frontend and open in your browser:

# from project root
python3 -m http.server 8080
# then open:
http://127.0.0.1:8080/index(withAI).html

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)  
- **Database:** SQLAlchemy (ORM)  
- **API Style:** RESTful  

### Contributors
- **Frontend:** Sriram Joshi  
- **Backend & API Design:** Jason Paz-Romero  

---

## 🚧 Project Status

This project is currently in **v1 / beta**.

- Database schema and API structure are **still evolving**
- Code organization is **not final**
- Some endpoints may be incomplete or inconsistent
- Performance and documentation improvements are planned

This version exists primarily as a **proof of concept and learning project**, with future updates intended to clean up architecture, improve scalability, and expand functionality.

---

## 🔮 Planned Improvements

- Improved database normalization and indexing  
- Cleaner project structure and modularization  
- Additional endpoints and datasets  
- Pagination, caching, and performance optimizations  
- Improved API documentation  
- Optional authentication and rate limiting  

---

## 📎 Notes

If parts of the codebase feel rough or poorly organized, that is expected at this stage. This project is actively evolving, and future versions will significantly improve structure, maintainability, and feature depth.

---
