# Screenshots

This folder contains screenshot evidence for the AWS IAM Auto Remediation Lab. These images are intended to show the final working detection, alerting, remediation, and troubleshooting flow across CloudTrail, CloudWatch, SNS, Lambda, and IAM.

## Suggested Screenshots to Include

### 1. CloudWatch Alarms
Show the configured alarms for:
- `CreateUserAlert`
- `CreateAccessKeyAlert`
- `AdminPolicyAlert`

Suggested files:
- `cloudwatch-alarms-overview.png`
- `cloudwatch-alarm-detail-createuser.png`

### 2. SNS Email Notifications
Show the remediation result emails delivered through the final notification path.

Suggested files:
- `sns-email-createuser.png`
- `sns-email-accesskey.png`
- `sns-email-adminpolicy.png`

### 3. Lambda Remediation Logs
Show successful Lambda execution logs for each scenario.

Suggested files:
- `lambda-log-createuser-success.png`
- `lambda-log-accesskey-success.png`
- `lambda-log-adminpolicy-success.png`

### 4. CloudTrail / Event Evidence
Show supporting event visibility for the IAM activity being detected.

Suggested files:
- `cloudtrail-createuser-event.png`
- `cloudtrail-createaccesskey-event.png`
- `cloudtrail-attachuserpolicy-event.png`

### 5. IAM Before / After Remediation Proof
Show the effect of the remediation action.

Suggested files:
- `iam-adminpolicy-before.png`
- `iam-adminpolicy-after.png`
- `iam-accesskey-before.png`
- `iam-accesskey-after.png`
- `iam-user-created-before-delete.png`
- `iam-user-after-delete.png`

### 6. Lambda / SNS Configuration Proof
Show the final working alerting and notification setup.

Suggested files:
- `lambda-function-overview.png`
- `sns-topics-overview.png`
- `securityalerts-lambda-topic.png`
- `securityalerts-email-topic.png`

## Purpose

These screenshots provide visual proof that the lab was not only configured, but successfully tested end-to-end.

They are intended to demonstrate:
- CloudTrail-backed IAM event detection
- CloudWatch alarm generation
- SNS alert routing
- Lambda-based remediation
- final remediation outcomes in IAM
- troubleshooting and architecture validation

## Notes

- Prefer screenshots that show successful remediation outcomes, not only setup pages.
- Before uploading to GitHub, crop or blur sensitive details such as account IDs, email addresses, or ARNs if needed.
- Use clear filenames so each screenshot is easy to map to a specific step in the workflow.
