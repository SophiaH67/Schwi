FROM python:3.10-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --force homeassistant_api==4.0.0.post2
COPY . .
CMD ["python", "main.py"]
