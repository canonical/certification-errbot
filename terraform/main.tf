resource "juju_application" "errbot" {
  name  = "errbot"
  model = var.juju_model

  charm {
    name     = "certification-errbot"
    channel  = var.channel
    revision = var.revision
  }

  config = {
    c3-client-id             = var.c3_client_id
    c3-client-secret         = var.c3_client_secret
    digest-send-time         = var.digest_send_time
    github-org               = var.github_org
    github-repositories      = var.github_repositories
    github-team              = var.github_team
    github-token             = var.github_token
    http-proxy               = var.http_proxy
    https-proxy              = var.https_proxy
    jira-current-sprint-only = var.jira_current_sprint_only
    jira-email               = var.jira_email
    jira-filter-id           = var.jira_filter_id
    jira-server              = var.jira_server
    jira-token               = var.jira_token
    ldap-base-dn             = var.ldap_base_dn
    ldap-bind-dn             = var.ldap_bind_dn
    ldap-bind-password       = var.ldap_bind_password
    ldap-server              = var.ldap_server
    log-level                = var.log_level
    mattermost-admins        = var.mattermost_admins
    mattermost-server        = var.mattermost_server
    mattermost-team          = var.mattermost_team
    mattermost-token         = var.mattermost_token
    no-proxy                 = var.no_proxy
  }
}
