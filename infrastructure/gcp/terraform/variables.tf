variable "github_repository_name" {
  description = "GitHub repository name: USER_NAME/REPO_NAME"
  type        = string
}

variable "github_user_name" {
  description = "GitHub user name from: USER_NAME/REPO_NAME"
  type        = string
}

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

variable "zone" {
  default     = ""
  description = "The GCP zone"
  type        = string
}
