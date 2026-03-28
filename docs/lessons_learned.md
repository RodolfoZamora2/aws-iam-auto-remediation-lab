# Lessons Learned

## Overview

This project was not just about building detection and remediation logic. A major part of its value came from troubleshooting how AWS services actually interact in a real cloud security workflow.

## Key Lessons

### 1. IAM is high risk
IAM actions are some of the most sensitive operations in AWS. Small changes such as creating users, creating access keys, or attaching high-privilege policies can have major security impact.

### 2. CloudTrail is critical for visibility
CloudTrail provided the foundation for detecting IAM activity in this lab. Without proper logging and event visibility, suspicious behavior would be difficult to detect and even harder to remediate.

### 3. Detection and remediation are different
It is possible to have CloudTrail, CloudWatch, SNS, and Lambda all partially working while the actual remediation still fails.

Early in the project, the workflow could:
- detect activity
- trigger alarms
- send SNS alerts
- invoke Lambda

But that did not automatically mean the risky IAM action was successfully remediated.

### 4. Detection requires proper filtering
Not every event matters equally. Filtering for specific IAM actions such as `CreateUser`, `CreateAccessKey`, and `AttachUserPolicy` was necessary to reduce noise and focus on higher-risk activity.

### 5. Permissions are everything
IAM roles and policies had to be configured correctly for the workflow to function end-to-end. Even small permission issues could break detection, prevent Lambda from taking action, or cause automation to fail unexpectedly.

### 6. CloudTrail lookup behavior matters
A major issue in the project was that Lambda was not always finding the expected CloudTrail event during remediation lookup.

This required:
- validating where events were being recorded
- checking CloudTrail Event History
- checking CloudWatch Logs log groups
- improving the Lambda lookup logic
- explicitly setting `CLOUDTRAIL_REGION`

This became one of the biggest troubleshooting points in the lab.

### 7. Region consistency and service alignment matter
A large part of troubleshooting involved understanding how CloudTrail, CloudWatch, SNS, and Lambda were interacting across the environment.

This reinforced the importance of:
- validating regional service configuration
- confirming where logs and events were being queried
- making sure the remediation workflow was aligned with the event source

### 8. Lambda retry timing and timeout settings matter
Earlier versions of the Lambda logic used retry behavior that was too slow relative to the configured timeout.

This caused cases where:
- Lambda received the alarm
- Lambda began event lookup
- Lambda timed out before completing remediation

Fixes included:
- reducing lookup retry delay
- tightening the retry count
- improving log visibility

### 9. Automated remediation needs safeguards
Once remediation started working, it became clear that safety controls mattered.

To reduce the chance of impacting important identities, the project was updated with:
- `PROTECTED_USERS`
- safer remediation checks
- clearer logging around what target was being acted on

This made the project safer and more realistic.

### 10. SNS design can create noisy loops
One issue was that Lambda was publishing result notifications back into the same SNS topic that was also being used to trigger Lambda.

That caused noisy behavior such as:
- Lambda receiving its own notification messages
- parse errors when the payload was not a CloudWatch alarm JSON message
- confusing extra log entries

This was fixed by separating SNS into two topics:
- `SecurityAlerts-Lambda` for CloudWatch alarm delivery to Lambda
- `SecurityAlerts-Email` for Lambda result notifications to Outlook

This made the workflow cleaner and easier to validate.

### 11. Troubleshooting is a real cloud security skill
A large part of this lab involved:
- debugging permissions
- fixing alert pipeline issues
- resolving service misconfigurations
- validating event detection before remediation
- testing the full workflow repeatedly

This reflected real-world cloud security work more than simply deploying services once.

### 12. End-to-end validation is critical
It was not enough to verify only one part of the pipeline.

A full successful test required confirming:
- the IAM action occurred
- CloudTrail recorded it
- CloudWatch metric filters and alarms detected it
- SNS delivered the alarm
- Lambda ran
- IAM remediation actually happened
- the result notification email was delivered

That full-chain validation is what turned the lab into a strong portfolio project.

## Final Results

By the end of the lab, all three core scenarios were working:

- `CreateUserAlert` → delete newly created IAM user
- `CreateAccessKeyAlert` → disable newest active access key
- `AdminPolicyAlert` → detach `AdministratorAccess`

## What I Would Improve Next

- tighten the Lambda IAM policy further for least privilege
- improve reporting and audit summaries
- expand detection coverage to additional IAM misuse scenarios
- add more structured error handling and logging
- add richer visuals and proof documentation

## Why This Project Was Valuable

This lab improved my understanding of:

- AWS detection and alerting workflows
- automated cloud response logic
- IAM abuse monitoring
- Lambda troubleshooting
- CloudTrail and CloudWatch integration
- the difference between “it triggers” and “it fully works”
