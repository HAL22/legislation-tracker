FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY src ./src

COPY resource ./resource

RUN mkdir -p /data

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]