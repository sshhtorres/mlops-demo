resource "google_iam_workload_identity_pool" "github_actions" {
  project                   = var.project_id
  workload_identity_pool_id = "github-actions"

  display_name = "GitHub Actions Pool"
  description  = "Pool for federating identities from GitHub Actions."
  disabled     = false

  depends_on = [
    google_project_service.services
  ]
}

resource "google_iam_workload_identity_pool_provider" "github_actions" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_actions.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-actions"

  attribute_condition = "attribute.repository == '${var.github_user_name}/${var.github_repository_name}'" # Restrict to specific GitHub repo
  description         = "OIDC provider for GitHub Actions to authenticate."
  disabled            = false
  display_name        = "GitHub Actions OIDC Provider"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
    "attribute.event_name" = "assertion.event_name"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
    allowed_audiences = []
    # allowed_audiences = ["${var.github_user_name}/${var.github_repository_name}"] # IMPORTANT: Adjust this if you use custom audience
  }

  depends_on = [
    google_iam_workload_identity_pool.github_actions
  ]
}
