FROM python:3.11

RUN apt-get update && apt-get install -y wget

ARG POSTGRES_USER
ARG POSTGRES_PASSWORD

ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

COPY generator .

RUN pip install uv

RUN uv pip install --system -r requirements.txt

CMD ["python", "generate.py"]