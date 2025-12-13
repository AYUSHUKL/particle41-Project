terraform {
  backend "s3" {
    bucket         = "simple-time-service-tfstate-12345"
    key            = "simple-time-service/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
