FROM python:3.11-slim

RUN apt-get update && apt-get install -y git curl wget gettext-base && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://getbruin.com/install/cli | sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /bruin

COPY bruin/bruin.yml.template .
COPY bruin/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]