# certification-errbot

Errbot plugins and a charm for deploying the Hardware Certification team's instance of https://github.com/errbotio/errbot

## Running locally

```bash
ERRBOT_SERVER=chat.canonical.com \
ERRBOT_ADMINS=@mz2 \
ERRBOT_TOKEN=... \
ERRBOT_TEAM=canonical uv run errbot
```

## Running tests

```bash
# Run all unit tests
uv run pytest tests

# Run specific test file
uv run pytest tests/test_pr_cache_refresh.py

# Run tests with verbose output
uv run pytest tests -v

# Run tests with coverage
uv run pytest tests --cov=plugins/certification
```

## Generating Test Observer and C3 libraries

Test Observer and C3 client libraries are built automatically as part of the OCI image.
For local development purposes, you need to execute the following at least once
(and whenever API changes of interest have happened):

```bash
./bin/generate-c3-client.sh
./bin/generate-test-observer-client.sh
```

## Running charm integration tests locally

```
cd charm
charmcraft test lxd
```