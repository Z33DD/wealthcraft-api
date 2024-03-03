# WealthCraft: Personal Budgeting App Backend

WealthCraft is a personal budgeting app designed to help users manage their finances effectively. This repository contains the backend code for WealthCraft. The backend is built using Python, FastAPI, Pydantic, and SQL.

## Features
### API Endpoints
The FastAPI-based backend exposes various endpoints for managing budget data, including:
- Creating and updating budget categories
- Adding and retrieving expenses
- Generating reports

### Database Schema
We use SQL (you can specify the specific database system you're using, such as PostgreSQL or SQLite) to store budget data. The schema includes tables for users, categories, and expenses.

### Pydantic Models
Pydantic models are used for data validation and serialization. These models ensure that incoming data adheres to the expected format.


## Installation
Clone the Repository:
```bash
git clone https://github.com/Z33DD/wealthcraft-api.git
cd wealthcraft-api
```

Install Dependencies using Poetry:
```bash
poetry install
```

## Database Setup:
- Create your database (e.g., PostgreSQL) and update the connection details in config.py.
- Run database migrations to create the necessary tables:

```bash
wealthcraft migrate
```

## Usage
Run the FastAPI Server:
```bash
wealthcraft serve
```

## API Documentation:
Visit http://localhost:5000/docs in your browser to explore the API endpoints using the interactive Swagger UI.

## Running with Docker
Build the Docker Image:
```bash
docker build -t wealthcraft-api .
```

Run the Docker Container:
```bash
docker run -p 5000:5000 wealthcraft-backend
```

## Contributing
Contributions are welcome! If you'd like to contribute to this project, follow these steps:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and submit a pull request.

## License
This project is licensed under the Unlicense - see the LICENSE file for details.
