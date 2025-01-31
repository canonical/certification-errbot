# hwcert-errbot



## Running locally

```bash
ERRBOT_SERVER=chat.canonical.com \
ERRBOT_ADMINS=@mz2 \
ERRBOT_TOKEN=... \
ERRBOT_TEAM=canonical uv run errbot
```

## Generating Test Observer client

```bash
./bin/generate-test-observer-client.sh
```

## Running charm integration tests locally

```
cd charm
charmcraft test lxd
```