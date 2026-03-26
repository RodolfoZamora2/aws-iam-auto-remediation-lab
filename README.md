AWS IAM Auto Remediation Lab
Overview

This project is a hands-on AWS cloud security lab focused on detecting suspicious IAM activity and testing auto-remediation workflows.

The lab simulates common IAM-based security events and uses AWS services to monitor, alert, and respond to those actions.

Objectives
Detect risky IAM activity in AWS
Generate alerts for suspicious behavior
Test Lambda-based remediation workflows
Build practical cloud security and SOC skills
Technologies Used
AWS Lambda
AWS IAM
AWS CloudTrail
AWS CloudWatch
AWS SNS
Security Scenarios Tested
Access key creation
AdministratorAccess policy attachment
Suspicious IAM-related activity monitoring
Response Logic

This lab includes Lambda-based remediation logic designed to respond to certain IAM security events, such as:

identifying newly created access keys
disabling or modifying risky IAM actions
testing policy-based response behavior
What I Learned
How IAM abuse can be detected in AWS
How CloudTrail logs user and policy activity
How CloudWatch can be used for alerting
How Lambda can be used for security response workflows
How to troubleshoot permissions, policies, and event-driven detection logic
Project Structure
aws-iam-auto-remediation-lab/
│
├── lambda/
│   └── auto_remediate.py
│
├── policies/
│   └── iam_policy.json
│
├── screenshots/
│
└── README.md
Screenshots

Add screenshots here of:

Lambda function
IAM policies
CloudWatch alarms
CloudTrail activity
test scenarios
Author

Rodolfo Zamora-Fuentes
