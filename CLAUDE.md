# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a certification-errbot project that provides Errbot plugins and a Juju charm for deploying the Hardware Certification team's instance of errbot on Mattermost. The bot integrates with C3 (Certification Database), Test Observer, GitHub, and LDAP for hardware certification workflow automation.

## Development Commands

### Local Development Setup
```bash
# Run the bot locally
ERRBOT_SERVER=chat.canonical.com \
ERRBOT_ADMINS=@mz2 \
ERRBOT_TOKEN=... \
ERRBOT_TEAM=canonical uv run errbot
```

### Generate API Client Libraries
Required for local development and when APIs change:
```bash
./bin/generate-c3-client.sh
./bin/generate-test-observer-client.sh
```

### Testing
```bash
# Run tests
uv run pytest

# Run charm integration tests
cd charm && charmcraft test lxd
```

### Package Management
```bash
# Install dependencies
uv sync

# Add new dependency
uv add package-name
```

## Architecture

### Core Components

- **Main Bot Plugin**: `plugins/certification/certification.py` - Primary errbot plugin with commands for artefacts, PRs, and machine lookup
- **Juju Charm**: `charm/src/charm.py` - Juju charm based Kubernetes deployment
- **Backend Integration**: Mattermost backend via `err-backend-mattermost` package

### Plugin Structure

The certification plugin (`plugins/certification/`) contains:
- `certification.py`: Main plugin with bot commands (`!artefacts`, `!prs`, `!cid`)
- `artefacts.py`: Test Observer artefact management and notifications
- `github.py`: GitHub API integration for PR management
- `ldap.py`: LDAP integration for user mapping
- `mattermost_api.py`: Mattermost API utilities
- `c3_auth.py`: C3 authentication handling
- `user_handle_cache.py`: User handle caching for performance

### External Integrations

- **C3 API**: Auto-generated client at `plugins/certification/c3/` for certification database access
- **Test Observer API**: Auto-generated client for test artefact tracking
- **GitHub API**: For PR monitoring across predefined repositories (checkbox, testflinger, hwcert-jenkins-jobs, certification-docs, certification-ops)
- **LDAP**: For mapping Mattermost usernames to GitHub accounts
- **Scheduled Jobs**: APScheduler for daily artefact digest notifications (Mon-Fri 9:00 UTC)

### Configuration

Environment variables are managed through:
- Local: Direct environment variables in `config.py`
- Charm: Juju configuration in `charm/charmcraft.yaml` passed to container environment

Required environment variables include:
- `ERRBOT_TOKEN`, `ERRBOT_SERVER`, `ERRBOT_TEAM`, `ERRBOT_ADMINS`
- `C3_CLIENT_ID`, `C3_CLIENT_SECRET`
- `GITHUB_TOKEN`, `GITHUB_ORG`
- `LDAP_SERVER`, `LDAP_BASE_DN`, `LDAP_BIND_DN`, `LDAP_BIND_PASSWORD`

### Testing Strategy

Tests use unittest with mocking for external API calls. Test configuration includes `conftest.py` for plugin path setup. Tests are located in `tests/` directory with main test file `test_artefacts_logic.py`.

## Key Bot Commands

- `!artefacts [filters]`: Display test artefacts with optional filtering
- `!prs [username]`: Show GitHub PRs assigned to user (auto-maps from Mattermost via LDAP)
- `!cid <canonical_id>`: Look up machine information from C3 database