resource "google_storage_bucket" "lake" {
  name     = "lake-${data.google_project.project.number}"
  location = var.region

  force_destroy               = true
  uniform_bucket_level_access = true
}
