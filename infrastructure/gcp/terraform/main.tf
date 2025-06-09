terraform {
  backend "gcs" {}

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.37.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone == "" ? "${var.region}-a" : var.zone
}

data "google_project" "project" {
}

resource "google_project_service" "services" {
  for_each = toset([
    "artifactregistry.googleapis.com",
    "iam.googleapis.com",
    "run.googleapis.com",
    "sts.googleapis.com", # Security Token Service API requerido para Workload Identity Federation
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}
