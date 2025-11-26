terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

variable "registry_id" {
  description = "ID of the Container Registry"
  type        = string
}

variable "folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
}

provider "yandex" {
  zone      = "ru-central1-a"
  folder_id = var.folder_id
  service_account_key_file = "key.json"
}

data "yandex_iam_service_account" "sa" {
  name = "registry-sa"
}

resource "yandex_serverless_container" "container" {
  name               = "test-simple-container"
  memory             = 256
  cores              = 1
  execution_timeout  = "30s"
  service_account_id = data.yandex_iam_service_account.sa.id
  
  image {
    url     = "cr.yandex/${var.registry_id}/devops_app:v1"
    command = ["gunicorn"]
    args    = ["--bind", "0.0.0.0:8080", "app:app"]
  }
}

resource "yandex_serverless_container_iam_binding" "invoker" {
  container_id = yandex_serverless_container.container.id
  role         = "serverless.containers.invoker"
  members      = ["system:allUsers"]
}

output "url" {
  value = "https://${yandex_serverless_container.container.id}.containers.yandexcloud.net"
}