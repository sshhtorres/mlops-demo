output "github_actions" {
  value = {
    service_account                 = google_service_account.github_actions_sa.email
    workload_identity_pool_provider = google_iam_workload_identity_pool_provider.github_actions.name
  }
}

output "github_repo" {
  value = "${var.github_user_name}/${var.github_repository_name}"
}

output "lake_storage_bucket_name" {
  value = google_storage_bucket.lake.name
}

output "project_id" {
  value = var.project_id
}

output "region" {
  value = var.region
}

output "services_artifact_registry_docker_repo" {
  value = {
    host = "${var.region}-docker.pkg.dev"
    url  = "${var.region}-docker.pkg.dev/${data.google_project.project.project_id}/${google_artifact_registry_repository.services_docker_repo.repository_id}"
  }
}
