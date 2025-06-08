resource "google_service_account" "github_actions_sa" {
  account_id   = "custom-github-actions-sa"
  display_name = "Custom GitHub Actions SA"
}

resource "google_project_iam_member" "github_actions_sa_roles_at_project_level" {
  for_each = toset([
    "roles/artifactregistry.writer",
    "roles/run.admin",
  ])

  project = var.project_id

  member = google_service_account.github_actions_sa.member
  role   = each.value
}

# brindar a la cuenta de servicio de GitHub Actions el permiso para impersonar la cuenta de servicio de Compute Engine
resource "google_service_account_iam_member" "github_actions_sa_act_as_compute_sa" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/${data.google_project.project.number}-compute@developer.gserviceaccount.com"

  member = google_service_account.github_actions_sa.member
  role   = "roles/iam.serviceAccountUser"
}

# brindar al proveedor de Workload Identity el permiso para impersonar la cuenta de servicio de GitHub Actions
resource "google_service_account_iam_member" "workload_identity_user_binding" {
  service_account_id = google_service_account.github_actions_sa.name

  member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_actions.name}/attribute.repository/${var.github_user_name}/${var.github_repository_name}"
  role   = "roles/iam.workloadIdentityUser"
}
