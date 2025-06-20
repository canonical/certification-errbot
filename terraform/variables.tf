variable "juju_model" {
  description = "Juju model to deploy this app in"
  type        = string
}

variable "mattermost_server" {
  description = "Chat server that mattermost will communicate on"
  type        = string
  default     = "chat.canonical.com"
}

variable "mattermost_admins" {
  description = "Comma separated usernames of mattermost admins"
  type        = string
}

variable "mattermost_token" {
  description = "Mattermost API token"
  type        = string
}

variable "mattermost_team" {
  description = "Mattermost team"
  type        = string
  default     = "canonical"
}

variable "c3_client_id" {
  description = "certification.canonical.com client ID"
  type        = string
}

variable "c3_client_secret" {
  description = ""
  type        = string
}

variable "log_level" {
  description = ""
  type        = string
  default     = "debug"
}