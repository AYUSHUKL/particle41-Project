# particle41-Project
Pre-Assement for Particle41

## Prerequisites

Before starting, ensure the following tools are installed:

- Git: https://git-scm.com/downloads
- Docker: https://docs.docker.com/get-docker/
- Terraform: https://developer.hashicorp.com/terraform/downloads
- AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
- An active AWS account

AWS resources will incur cost. Please clean up after testing.

## AWS Credentials Configuration

Terraform and CI/CD require AWS credentials.

To configure locally:
aws configure

For CI/CD, AWS credentials are stored securely as GitHub Actions secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION

No credentials are committed to this repository.


##### Task 1 - Minimalist Application Development / Docker / Kubernetes ####

1️⃣ Application Code (app.py)

The project starts with a simple Python web application.

Uses FastAPI

Stateless

Listens on port 8080

Returns current timestamp and client IP


2️⃣ Dockerfile (Containerization)

The application is packaged into a container using a Dockerfile.


Important Docker practices used

Runs as a non-root user

Uses a lightweight base image

Exposes only the required port



3️⃣ Docker Image Creation

After building, the application becomes a Docker image.

>What the image contains

Application code

Python runtime

Required dependencies

Commands:
    cd app
    docker build -t simpletimeservice:v1 .


4️⃣ Push Docker Image to Registry (Docker Hub)

The image is pushed to Docker Hub, which acts as a central registry. 
## make sure you have account in docker hub

Commands
        docker push ayushukl/simpletimeservice:v1

>Why this step is required

ECS needs a registry to pull images from

CI/CD pipelines must access the image

Decouples build from deployment

>To Run docker image in your system
    command:
    docker run -p 8080:8080 ayushukl/simpletimeservice:v1

##### Task 2 - Terraform and Cloud: create the infrastructure to host your container. #####

1️⃣ Terraform Backend & State Locking (Before Infrastructure Creation)

    Before creating any AWS resources, we first prepare Terraform’s remote backend.

    This is a critical step and must be completed before running Terraform.

    🔐 Terraform State Problem (Without Remote Backend)

        If Terraform state is stored locally:

        CI/CD pipelines cannot work reliably

        Multiple users or jobs can overwrite state

        No locking mechanism exists

        Infrastructure state can become corrupted

        To solve this, Terraform state is stored remotely and locked during execution.

2️⃣ Create S3 Bucket (Terraform State Storage)

    Terraform stores its state file (terraform.tfstate) in an S3 bucket.
Commands:
        aws s3api create-bucket --bucket simple-time-service-tfstate-12345 --region ap-south-1 --create-bucket-configuration LocationConstraint=ap-south-1

3️⃣ Enable S3 Versioning (State History & Recovery)
    Versioning ensures that all previous versions of the Terraform state file are preserved.

Commands:
        aws s3api put-bucket-versioning --bucket simple-time-service-tfstate-12345 --versioning-configuration Status=Enabled

4️⃣ Create DynamoDB Table (Terraform State Locking)

    DynamoDB is used to lock the Terraform state during execution.

Commands:
        aws dynamodb create-table --table-name terraform-locks --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST
5️⃣ Terraform Initialization

    After backend and locking setup, Terraform must be initialized.
Commands:
    cd terraform
    terraform init

6️⃣ Terraform Infrastructure Creation

Terraform provisions AWS resources in a defined order.

    Terraform
  ├── VPC
  │   ├── Public Subnets (ALB)
  │   └── Private Subnets (ECS)
  ├── NAT Gateway
  ├── Security Groups
  ├── Application Load Balancer
  ├── Target Group
  ├── ECS Cluster
  ├── Task Definition
  └── ECS Service

Commands:
    terraform plan
    terraform apply

7️⃣ CI/CD Automation
    On every push to the main branch:
    GitHub Push
         ↓
    Build Docker Image
         ↓
    Push to Docker Hub
         ↓
    Terraform Init
         ↓
    Terraform Plan
         ↓
    Terraform Apply

8️⃣ Verification

After deployment completes, Terraform outputs the ALB DNS name.

Test the service
    http://simple-time-service-alb-1801556568.ap-south-1.elb.amazonaws.com





## Cleanup

To avoid AWS charges:
cd terraform
terraform destroy

After destroy, delete:
- S3 backend bucket
- DynamoDB lock table



## Flow Diagram:
  ![alt text](image-1.png)