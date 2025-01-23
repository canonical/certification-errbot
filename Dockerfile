# Use the specified base image
FROM ubuntu:24.04
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

LABEL name="hwcert-errbot" \
    version="6.2.0" \
    description="An OCI image for hwcert-errbot" \
    license="GPL-3.0"

RUN apt-get update && \
    apt-get install -y python3.12 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

WORKDIR /app

COPY . .

RUN cargo install --git https://github.com/astral-sh/uv uv
COPY config/config.py /root/

ENTRYPOINT ["/app/venv/bin/errbot"]

CMD uv run errbot
