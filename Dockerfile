FROM python:3.9-slim

# 1. Change this to a neutral workspace directory
WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. This copies your 'app' folder into '/workspace/app'
COPY . .

# 3. Uvicorn runs from /workspace, finds the 'app' folder, and succeeds!
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
