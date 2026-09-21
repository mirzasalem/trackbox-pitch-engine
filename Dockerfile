FROM python:3.12-slim

WORKDIR /app

# opencv-python needs these system libs at import time even though it's a
# pure pip package; python:3.12-slim doesn't ship them.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
