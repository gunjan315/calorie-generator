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

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

- `controllers/` - Request handlers
- `services/` - Business logic
- `models/` - Data models
- `database/` - Database connections
- `middleware/` - Custom middleware
- `routes/` - API endpoints