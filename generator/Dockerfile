FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

COPY generator .

RUN pip install uv

RUN uv pip install --system -r requirements.txt

CMD ["python", "generate.py"]
