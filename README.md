# Clone repository

git clone https://github.com/Niraj12chaudhary/Book-Review-System.git
cd book-review-service

# Create virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt

# Set environment variables

export DATABASE_URL="postgresql://user:password@localhost:5432/bookreviews"
export REDIS_URL="redis://localhost:6379"

# Run migrations

alembic upgrade head

# Start the server

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
