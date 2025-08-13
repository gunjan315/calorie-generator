# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt

# Run MongoDB in Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:latest

  # Run with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or run the main.py file
python calorie_count_generator.main.py