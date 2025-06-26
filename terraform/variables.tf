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

variable "no_proxy" {
  description = "Resources that we should abe able to access bypassing proxy"
  type        = string
  default     = "localhost,127.0.0.1,::1"
}
