FROM python:3.11

RUN apt-get update && apt-get install -y git curl wget gettext-base && rm -rf /var/lib/apt/lists/*

# Pin the CLI. With no tag the installer takes whatever is newest, so an
# unpinned build is not reproducible; it fails loudly on an unknown tag.
ARG BRUIN_VERSION=v0.11.757

RUN curl -LsSf https://getbruin.com/install/cli | sh -s -- "${BRUIN_VERSION}"

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /bruin

COPY bruin/bruin.yml.template .
COPY bruin/entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]