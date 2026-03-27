# AWS IAM Auto Remediation Lab

A hands-on AWS cloud security project focused on detecting and automatically remediating risky IAM activity using CloudTrail, CloudWatch, SNS, Lambda, and IAM.

## Project Overview

This lab simulates common IAM-related security events and builds an automated response workflow to detect, alert on, and remediate them.

The project monitors risky IAM actions, triggers CloudWatch alarms from CloudTrail-backed activity, routes alerts through SNS, and invokes a Lambda function that performs targeted remediation steps.

## Objectives

- Detect suspicious IAM activity in AWS
- Generate alerts for risky IAM behavior
- Automatically remediate selected IAM actions
- Practice real cloud security monitoring and response workflows
- Build hands-on SOC and cloud security project experience

## AWS Services Used

- AWS IAM
- AWS CloudTrail
- AWS CloudWatch
- AWS SNS
- AWS Lambda

## Security Scenarios Tested

This lab was built and tested around three IAM-related scenarios:

1. **CreateUser**
   - Detect when a new IAM user is created
   - Automatically delete the newly created user

2. **CreateAccessKey**
   - Detect when a new access key is created
   - Automatically disable the newest active access key for that user

3. **AttachUserPolicy / AdministratorAccess**
   - Detect when the `AdministratorAccess` managed policy is attached to a user
   - Automatically detach the policy

## Final Working Detection and Remediation Flow

IAM action occurs  
→ CloudTrail records the event  
→ CloudWatch Logs / metric filter detects the event  
→ CloudWatch alarm enters ALARM state  
→ SNS topic (`SecurityAlerts-Lambda`) sends the alarm to Lambda  
→ Lambda looks up the matching CloudTrail event  
→ Lambda performs remediation in IAM  
→ Lambda publishes a result notification to SNS topic (`SecurityAlerts-Email`)  
→ Email notification is delivered to Outlook

## Remediation Logic

The Lambda function performs the following actions:

- Deletes newly created IAM users for `CreateUser` alerts
- Disables the newest active access key for `CreateAccessKey` alerts
- Detaches `AdministratorAccess` for admin policy attachment alerts

The function also includes safety improvements such as:

- protected usernames via `PROTECTED_USERS`
- configurable CloudTrail lookup region via `CLOUDTRAIL_REGION`
- retry-based event lookup logic
- improved debug and remediation logging

## Key Improvements Made During the Lab

This project evolved significantly during testing and troubleshooting. Final improvements included:

- fixing CloudTrail event lookup behavior by querying the correct region
- shortening retry timing to avoid Lambda timeout issues
- adding protected-user safeguards to avoid remediating sensitive usernames
- improving logging for event lookup and remediation results
- separating SNS into two topics:
  - `SecurityAlerts-Lambda` for CloudWatch alarm delivery to Lambda
  - `SecurityAlerts-Email` for Lambda notification emails

This SNS split prevented Lambda from receiving and attempting to parse its own notification messages.

## Lessons Learned

This lab helped reinforce several important cloud security concepts:

- CloudTrail event lookup and regional behavior can affect response logic
- CloudWatch alarms and SNS routing need clean design to avoid noisy event loops
- Lambda retry timing and timeout values matter in real workflows
- Automated remediation should include safeguards to avoid impacting protected identities
- Detection is not enough on its own; response logic must be validated end-to-end

## Repository Structure

```text
aws-iam-auto-remediation-lab/
├── README.md
├── lambda/
│   └── auto_remediate.py
├── policies/
│   └── iam_policy.json
├── docs/
│   ├── architecture.md
│   └── lessons_learned.md
└── screenshots/
    └── README.md

## Author

**Rodolfo Zamora-Fuentes**
