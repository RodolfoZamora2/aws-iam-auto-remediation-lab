# AWS IAM Auto Remediation Lab - Architecture

## Overview
This project demonstrates a cloud security workflow for detecting suspicious IAM activity in AWS, generating alerts, and testing basic Lambda-based auto-remediation actions.

The lab was built to simulate how a SOC or cloud security team could monitor IAM-related risks and respond to potentially dangerous administrative actions.

---

## Objective
The goal of this lab was to:

- Detect suspicious IAM-related activity
- Trigger security alerts
- Investigate whether automation could respond to risky events
- Practice AWS security engineering and cloud monitoring concepts

---

## Core AWS Services Used

### 1. AWS CloudTrail
Used to log account activity and API calls related to IAM actions.

Examples of monitored activity:
- AttachUserPolicy
- CreateUser
- DeleteUser
- CreateAccessKey
- PutUserPolicy

---

### 2. Amazon CloudWatch
Used to monitor logs and generate alarms based on suspicious IAM-related actions.

CloudWatch helped simulate how defenders can create security detections for risky behavior inside AWS.

---

### 3. AWS Lambda
Used to test automation logic for handling specific IAM events.

The Lambda function was designed to:
- Review suspicious IAM activity
- Attempt basic remediation logic
- Publish alerts for visibility
- Support future automation improvements

---

### 4. Amazon SNS
Used to send alert notifications when suspicious activity was detected.

SNS acted as the notification layer for the lab.

---

## High-Level Workflow

1. A suspicious IAM-related action occurs in AWS
2. CloudTrail records the event
3. CloudWatch detects the activity through filtering and alarms
4. SNS sends an alert notification
5. Lambda can be used to review or respond to the event

---

## Security Scenarios Tested

This lab focused on high-risk IAM behavior such as:

- Admin policy attachment
- Suspicious user creation
- Access key abuse scenarios
- Unauthorized or risky IAM changes

---

## Remediation Concept
This project explores the concept of **auto-remediation**, where a cloud environment can automatically react to risky security events.

Examples of remediation ideas include:

- Disabling compromised access keys
- Removing high-risk policy attachments
- Deleting suspicious IAM users
- Sending immediate security alerts to responders

---

## Skills Demonstrated

This lab demonstrates hands-on experience with:

- AWS IAM
- AWS CloudTrail
- Amazon CloudWatch
- AWS Lambda
- Amazon SNS
- Security monitoring
- Detection engineering
- Cloud incident response concepts
- Basic security automation

---

## Notes
This project is a learning and portfolio lab designed to demonstrate cloud security detection and response concepts.

It is not intended to represent a production-ready enterprise deployment, but it shows practical understanding of how AWS-native security tooling can be used in a SOC-style workflow.
