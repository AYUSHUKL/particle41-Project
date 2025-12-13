# particle41-Project
Pre-Assement for Particle41


create s3 bucket

aws s3api create-bucket --bucket simple-time-service-tfstate-12345 --region ap-south-1 --create-bucket-configuration LocationConstraint=ap-south-1

Enable Versoning
aws s3api put-bucket-versioning --bucket simple-time-service-tfstate-12345 --versioning-configuration Status=Enabled

Create Dynamodb Table (Locking)

aws dynamodb create-table --table-name terraform-locks --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST
