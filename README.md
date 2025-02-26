# AWS CLI Automation Tool

This tool allows for automated management of AWS resources through a Command Line Interface (CLI). It includes capabilities for managing EC2, S3, and Route 53, while also checking if dependencies (such as `boto3` and `awscli`) are installed and if not, installs them. The tool also provides the user with an option to configure AWS credentials if not already done.

## Features
- **Automatic Dependency Installation**: If `boto3` or `awscli` are not installed, the script prompts the user to install them.

- **AWS CLI Configuration Check**: The script checks whether the AWS CLI is configured. If not, the user will be prompted to configure their AWS credentials (Access Key, Secret Key, Region).
  
- **EC2**:
  - Create new EC2 instances (with options to choose between different instance types and AMIs).
  - Start EC2 instances.
  - Stop EC2 instances.
  - List EC2 instances that were created.
  
- **S3**:
  - Create S3 Buckets (with ACL options for public or private access).
  - Upload files to S3 Buckets.
  - List S3 Buckets created through this tool.

- **Route53**:
  - Create Hosted Zones.
  - Perform DNS Record actions such as CREATE, DELETE, and UPSERT.
  - Validate domain names and manage DNS records associated with Hosted Zones.


## Requirements

- Python 3.x
- `boto3` (AWS SDK for Python) 
- `awscli` (AWS Command Line Interface)

## Setup

Before running the tool, ensure you have Python 3 installed. You can install the necessary dependencies by following the instructions below:

### Step 1: Install Dependencies

If you don't have `boto3` or `awscli` installed, the script will prompt you to install them. Alternatively, you can install them manually using the following commands:

```bash
pip install boto3
pip install awscli
```

### Step 2: Configure AWS CLI

The script will check if the AWS CLI is configured. If it's not, you will be prompted to provide the following AWS credentials:

- **AWS Access Key ID**
- **AWS Secret Access Key**
- **AWS Region**

You can configure these credentials manually by running the following command:

```bash
aws configure
```

You will be prompted to enter your AWS Access Key ID, Secret Access Key, Default Region Name, and Default Output Format.

### Step 3: Run the Script

Run the Python script to interact with AWS services:

```bash
python main.py
```

Once the script is executed, you will be prompted to choose an action:

### EC2 Operations:
- `[1] Create EC2 Instances`: Create a new EC2 instance with options to select the instance type (e.g., `t3.nano`, `t4g.nano`) and AMI (e.g., Ubuntu, Amazon Linux).
- `[2] Start EC2 Instance`: Start a stopped EC2 instance.
- `[3] Stop EC2 Instance`: Stop a running EC2 instance.
- `[4] List EC2 Instances`: View all EC2 instances created through this CLI.


### S3 Operations:
- `[1] Create S3 Bucket`: Create a new S3 bucket by specifying a name and setting the ACL (Access Control List) to either public or private.
- `[2] Upload File to S3`: Upload a file to an S3 bucket. You will be asked to select a bucket, provide the file path, and optionally specify an object name.
- `[3] List S3 Buckets`: List all S3 buckets that have been created through this CLI.


### Route 53 Operations:
- `[1] Create Hosted Zone`: Create a new DNS hosted zone by providing a domain name.
- `[2] Action on DNS Record`: Perform an action (CREATE, DELETE, UPSERT) on a DNS record associated with a hosted zone. You can specify the TTL (Time To Live) and the IP address for the record.

---

This tool gives you the ability to perform a variety of tasks related to EC2, S3, and Route 53, making it a valuable resource for automating AWS management tasks directly from the command line.





