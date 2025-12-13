variable "aws_region" {
  default = "ap-south-1"
}

variable "project_name" {
  default = "simple-time-service"
}

variable "container_image" {
  description = "Docker image"
  type        = string
}

variable "container_port" {
  default = 8080
}

variable "desired_count" {
  default = 2
}
