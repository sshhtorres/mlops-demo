resource "google_artifact_registry_repository" "services_docker_repo" {
  format        = "DOCKER"
  description   = "Docker repository for GitHub Actions container images"
  repository_id = "services-repo"

  location = var.region
  project  = var.project_id

  depends_on = [
    google_project_service.services
  ]
}

resource "google_artifact_registry_repository_iam_member" "sa_artifact_writer" {
  location   = google_artifact_registry_repository.services_docker_repo.location
  repository = google_artifact_registry_repository.services_docker_repo.name

  member = "serviceAccount:${google_service_account.github_actions_sa.email}"
  role   = "roles/artifactregistry.writer"
}
