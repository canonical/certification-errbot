resource "juju_application" "errbot" {
  name  = "errbot"
  model = var.juju_model

  charm {
    name    = "certification-errbot"
    channel = "latest/edge"
  }

  config = {
    c3-client-id             = var.c3_client_id
    c3-client-secret         = var.c3_client_secret
    digest_send_time         = var.digest-send-time
    github_org               = var.github-org
    github_repositories      = var.github-repositories
    github_team              = var.github-team
    github_token             = var.github-token
    http-proxy               = var.http_proxy
    https-proxy              = var.https_proxy
    jira-current-sprint-only = var.jira_current_sprint_only
    jira_email               = var.jira-email
    jira_filter_id           = var.jira-filter
    jira_server              = var.jira-server
    jira_token               = var.jira-token
    ldap_base_dn             = var.ldap-base-dn
    ldap_bind_dn             = var.ldap-bind-dn
    ldap_bind_password       = var.ldap-bind-password
    ldap_server              = var.ldap-server
    log-level                = var.log_level
    mattermost-admins        = var.mattermost_admins
    mattermost-server        = var.mattermost_server
    mattermost-team          = var.mattermost_team
    mattermost-token         = var.mattermost_token
    no-proxy                 = var.no_proxy
  }
}
