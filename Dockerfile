# Use the specified base image
FROM ubuntu:22.04
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV ERRBOT_TOKEN=""
ENV ERRBOT_TEAM="Canonical"
ENV ERRBOT_ADMIN=""
ENV ERRBOT_SERVER="chat.canonical.com"

LABEL name="certification-errbot" \
    version="6.2.0" \
    description="An OCI image for certification-errbot" \
    license="GPL-3.0"

RUN apt-get update && \
    apt-get install -y python3.12 python3.12-gdbm git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN mkdir -p data

ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

RUN uv sync
RUN uv tool install errbot

RUN ./bin/generate-c3-client.sh
RUN ./bin/generate-test-observer-client.sh

CMD ["uv", "run", "errbot"]
