resource "juju_application" "errbot" {
  name  = "errbot"
  model = var.juju_model

  charm {
    name    = "certification-errbot"
    channel = "latest/edge"
  }

  config = {
    log-level         = var.log_level
    mattermost-team   = var.mattermost_team
    mattermost-server = var.mattermost_server
    mattermost-token  = var.mattermost_token
    mattermost-admins = var.mattermost_admins
    c3-client-id      = var.c3_client_id
    c3-client-secret  = var.c3_client_secret
    http-proxy        = var.http_proxy
    https-proxy       = var.https_proxy
    no-proxy          = var.no_proxy
  }
}
