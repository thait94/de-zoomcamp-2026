terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = "project-378b4ffb-57b4-4f0b-ter91f"
  region  = "us-central1"

}

resource "google_storage_bucket" "test-bucket" {
  name     = "project-378b4ffb-57b4-4f0b-91f-terra-bucket"
  location = "US"

  # Optional, but recommended settings:
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}
