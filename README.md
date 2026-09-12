# Serverless File Processing Pipeline (Terraform)

## 📌 Project Overview
Built a fully serverless file processing pipeline on AWS, entirely provisioned with Terraform instead of the console. A file uploaded to S3 automatically triggers a Lambda function that reads its metadata and writes a record to DynamoDB, with CloudWatch and SNS monitoring the pipeline for failures. This project demonstrates Infrastructure as Code, serverless architecture, and event-driven design, closing gaps my earlier console-based projects didn't cover.

---

## ☁️ AWS Services Used
- **Amazon S3** – Storage and event source for uploaded files
- **AWS Lambda (Python)** – Processes each uploaded file and extracts metadata
- **Amazon DynamoDB** – Stores processed file records
- **Amazon CloudWatch** – Monitors Lambda execution and errors
- **Amazon SNS** – Delivers email alerts on pipeline failure
- **AWS IAM** – Least-privilege role and policy scoping exactly what the Lambda function can access
- **Terraform** – Provisions all of the above as code

---

## ⚙️ Key Implementations
- Wrote the entire infrastructure (S3 bucket, IAM role and policy, Lambda function, DynamoDB table, CloudWatch alarm, SNS topic) as Terraform configuration instead of clicking through the console
- Built a Python Lambda function that reads S3 event metadata (bucket, key, size, content type) and writes a structured record to DynamoDB
- Configured an S3 event notification to automatically invoke the Lambda function on every new upload
- Scoped IAM permissions to exactly three actions the Lambda function needs (read S3, write DynamoDB, write CloudWatch logs), following the same least-privilege principle as my earlier projects
- Configured a CloudWatch alarm on Lambda errors with an SNS email subscription for failure alerting
- Verified the entire pipeline end to end with a real test upload before considering it complete

---

## 🐛 Troubleshooting & Fixes

**Issue 1 — Terraform apply failed with "No valid credential sources found"**
Ran `terraform plan` before AWS CLI credentials were configured on the machine. Diagnosed by running `aws configure list` (confirmed no keys were set) and `aws sts get-caller-identity` (confirmed the fix once resolved). Fixed by generating an IAM access key and running `aws configure`.

**Issue 2 — Access Denied errors on S3 and IAM resource creation**
`terraform apply` authenticated successfully but failed with `Access Denied` on both `s3:CreateBucket` and `iam:CreateRole`. This confirmed a distinction worth knowing: valid credentials and sufficient permissions are two separate things. The IAM user had no policies attached yet. Resolved by attaching the appropriate permissions policy to the user in IAM.

**Issue 3 — Oversized file blocked the GitHub push**
After committing, `git push` was rejected because a 773 MB Terraform provider binary (downloaded locally by `terraform init`) had been committed in an early commit, exceeding GitHub's 100 MB file limit. Removing the file from the working directory wasn't enough, since Git still retained it in history. Resolved by deleting local Git history entirely and recommitting with a corrected `.gitignore` in place from the first commit, keeping build artifacts and provider binaries out of version control going forward.

---

## 🚀 Key Outcomes
- Built and deployed a working serverless pipeline entirely through Infrastructure as Code
- Verified the full event chain end to end: S3 upload → Lambda execution → DynamoDB write, confirmed via CloudWatch Logs and the DynamoDB console
- Practiced real-world Git hygiene: correcting a `.gitignore` mistake and cleaning bad history before it reached a public repository
- Tore down all resources with `terraform destroy` after validation, avoiding ongoing costs, the same cost-awareness principle tested in the AWS Solutions Architect exam

---

## 🧠 Skills Demonstrated
- Infrastructure as Code (Terraform)
- Serverless Architecture (Lambda, event-driven design)
- AWS IAM Least-Privilege Policy Design
- Python (boto3, Lambda handler logic)
- CloudWatch Monitoring & SNS Alerting
- Git/GitHub Version Control & History Management
- Troubleshooting & Root-Cause Diagnosis

---

## 📸 Screenshots

### CloudWatch Alarm
![CloudWatch Alarm](https://github.com/tylertbrice12-hue/serverless-pipeline-project/blob/main/cloudwatch-alarm.png?raw=true)

### DynamoDB Item
![DynamoDB Item](https://github.com/tylertbrice12-hue/serverless-pipeline-project/blob/main/dynamodb-item.png?raw=true)

### Lambda Function Overview
![Lambda Overview](https://github.com/tylertbrice12-hue/serverless-pipeline-project/blob/main/lambda-overview.png?raw=true)

### S3 Bucket
![S3 Bucket](https://github.com/tylertbrice12-hue/serverless-pipeline-project/blob/main/s3-bucket.png?raw=true)

### SNS Subscription
![SNS Subscription](https://github.com/tylertbrice12-hue/serverless-pipeline-project/blob/main/sns-subscription.png?raw=true)

---

## 🔗 Notes
This project was built to specifically close the Terraform and Lambda/scripting gaps identified across several job applications. Unlike my first two console-based projects, every resource here is defined as code, version-controlled, and fully reproducible with `terraform apply`.
