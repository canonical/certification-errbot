variable "c3_client_id" {
  description = "certification.canonical.com client ID"
  type        = string
}

variable "c3_client_secret" {
  description = "certification.canonical.com client secret"
  type        = string
}

variable "digest_send_time" {
  description = "Time to send the daily digest in HH:MM format (24-hour, UTC). For example: \"09:00\" for 9am UTC."
  type        = string
  default     = "06:30"
}

variable "github_org" {
  description = "GitHub organization name to fetch PRs from"
  type        = string
  default     = "canonical"
}

variable "github_repositories" {
  description = "Comma-separated list of repository names to monitor for PRs. If not set, uses default list."
  type        = string
  default     = ""
}

variable "github_team" {
  description = "GitHub team name to send daily PR notifications for. Team members will receive PR summaries at 9am UTC Mon-Fri."
  type        = string
}

variable "github_token" {
  description = "GitHub personal access token for API access"
  type        = string
}

variable "http_proxy" {
  description = "HTTP proxy for accessing external HTTP resources"
  type        = string
  default     = ""
}

variable "https_proxy" {
  description = "HTTPS proxy for accessing external HTTPS resources"
  type        = string
  default     = ""
}

variable "jira_current_sprint_only" {
  description = "Filtering by current sprint when fetching jira issues"
  type        = bool
  default     = false
}

variable "jira_email" {
  description = "Jira email address for API access"
  type        = string
}

variable "jira_filter_id" {
  description = "Jira filter ID to use for fetching issues"
  type        = string
}

variable "jira_server" {
  description = "Jira server URL for issue tracking integration"
  type        = string
}

variable "jira_token" {
  description = "Jira API token for authentication"
  type        = string
}

variable "juju_model" {
  description = "Juju model to deploy this app in"
  type        = string
}

variable "ldap_base_dn" {
  description = "LDAP base DN for user searches"
  type        = string
}

variable "ldap_bind_dn" {
  description = "LDAP bind DN for authentication"
  type        = string
}

variable "ldap_bind_password" {
  description = "LDAP bind password for authentication"
  type        = string
}

variable "ldap_server" {
  description = "LDAP server URL for user lookups"
  type        = string
}

variable "log_level" {
  description = "Charm log level"
  type        = string
  default     = "debug"
}

variable "mattermost_admins" {
  description = "Comma separated usernames of mattermost admins"
  type        = string
}

variable "mattermost_server" {
  description = "Chat server that mattermost will communicate on"
  type        = string
  default     = "chat.canonical.com"
}

variable "mattermost_team" {
  description = "Mattermost team"
  type        = string
  default     = "canonical"
}

variable "mattermost_token" {
  description = "Mattermost API token"
  type        = string
}

variable "no_proxy" {
  description = "Resources that we should abe able to access bypassing proxy"
  type        = string
  default     = "localhost,127.0.0.1,::1"
}

variable "channel" {
  description = "Juju charm channel to use"
  type        = string
  nullable    = true
  default     = null
}

variable "revision" {
  description = "Revision of the charm to use"
  type        = number
  nullable    = true
  default     = null
}
