# particle41-Project
Pre-Assement for Particle41

## Prerequisites
Before starting, ensure the following tools are installed:

Git – https://git-scm.com/downloads

Docker – https://docs.docker.com/get-docker/

Terraform – https://developer.hashicorp.com/terraform/downloads

AWS CLI – https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

An active AWS account

> AWS resources will incur cost. Please clean up after testing.

> AWS Credentials Configuration

Terraform and CI/CD require AWS credentials.

Configure locally
aws configure

For CI/CD (GitHub Actions)

Store credentials as GitHub Actions secrets:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

DOCKERHUB_USERNAME

DOCKERHUB_TOKEN

> No credentials are committed to this repository.

##### Task 1 - Minimalist Application Development / Docker / Kubernetes ####

1️⃣ Application Code (app.py)

A simple Python web application using FastAPI.

Characteristics:

Stateless

Listens on port 8080

Returns:

Current timestamp

Client IP address

2️⃣ Dockerfile (Containerization)

The application is packaged into a Docker container.

Best practices used:

Runs as a non-root user

Uses a lightweight base image

Exposes only the required port

3️⃣ Build Docker Image
cd app
docker build -t simpletimeservice:v1 .

4️⃣ Push Docker Image to Docker Hub

Make sure you have a Docker Hub account.

docker push ayushukl/simpletimeservice:v1


Why this is required:

ECS needs a registry to pull images

CI/CD pipelines require image access

Decouples build from deployment

5️⃣ Run Docker Image Locally (Optional)
docker run -p 8080:8080 ayushukl/simpletimeservice:v1

##### Task 2 - Terraform and Cloud: create the infrastructure to host your container. #####

1️⃣ Terraform Backend & State Locking (Before Infrastructure Creation)

Terraform state must not be stored locally for CI/CD workflows.

Problems with local state:

CI/CD pipelines cannot work reliably

Multiple users/jobs can overwrite state

No locking mechanism

State corruption risk

To solve this, Terraform uses:

S3 → Remote state storage

DynamoDB → State locking

2️⃣ Create S3 Bucket (Terraform State Storage)
aws s3api create-bucket \
  --bucket simple-time-service-tfstate-12345 \
  --region ap-south-1 \
  --create-bucket-configuration LocationConstraint=ap-south-1


Why S3:

Highly durable

Shared storage

Native Terraform support

3️⃣ Enable S3 Versioning (State History & Recovery)
aws s3api put-bucket-versioning \
  --bucket simple-time-service-tfstate-12345 \
  --versioning-configuration Status=Enabled


Benefits:

Protects against accidental deletion

Allows rollback of broken deployments

Maintains state history

4️⃣ Create DynamoDB Table (Terraform State Locking)
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST


How locking works:

Terraform creates a lock before execution

Other runs wait or fail

Lock is released after completion

5️⃣ Terraform Initialization
cd terraform
terraform init


What happens:

Backend connection is established

Providers are downloaded

State locking is verified

6️⃣ Terraform Infrastructure Creation
terraform plan
terraform apply


Resources provisioned:

VPC
├── Public Subnets (ALB)
├── Private Subnets (ECS)
├── NAT Gateway
├── Security Groups
├── Application Load Balancer
├── Target Group
├── ECS Cluster
├── Task Definition
└── ECS Service


Result:
The application is public, but the containers remain private and secure.

🔄 CI/CD Automation

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


No manual deployment steps are required.

> Verification

After deployment completes, Terraform outputs the ALB DNS name.

Test the service
    http://simple-time-service-alb-1801556568.ap-south-1.elb.amazonaws.com


Expected response:
{
  "timestamp": "2025-12-13T10:29:04.309550+00:00",
  "ip": "106.215.176.112"
}

## Cleanup (IMPORTANT)

To avoid AWS charges:

cd terraform
terraform destroy


After destroy, manually delete:

S3 backend bucket

DynamoDB lock table
