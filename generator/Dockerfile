FROM python:3.11-slim

COPY generator .

RUN pip install uv

RUN uv pip install --system -r requirements.txt

CMD ["python", "generate.py"]
