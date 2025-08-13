# Calorie Counter API

A FastAPI-based calorie counting application that integrates with the USDA Food Database API.

## Features

- JWT authentication
- Rate limiting
- Fuzzy matching for food items
- MongoDB integration
- USDA API integration

## Setup

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
API_KEY=your_usda_api_key
JWT_KEY=your_jwt_secret_key_at_least_32_chars

4. Run MongoDB:
```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

5. Start the application:
```bash
uvicorn main:app --reload
```

## API Documentation

- **Local:** `http://localhost:8000/docs`
- **Live:** [https://calorie-generator-production.up.railway.app/docs](https://calorie-generator-production.up.railway.app/docs)

## Project Structure

- `controllers/` - Request handlers
- `services/` - Business logic
- `models/` - Data models
- `database/` - Database connections
- `middleware/` - Custom middleware
- `routes/` - API endpoints

## Deployment

This application is deployed on Railway using Docker. The deployment includes:
- FastAPI application container
- MongoDB database service
- Automatic environment variable management