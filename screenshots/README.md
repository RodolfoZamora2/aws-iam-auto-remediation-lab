# Screenshots

This folder contains screenshot evidence for the AWS IAM Auto Remediation Lab. The screenshots are organized by remediation scenario to show the final working detection, alerting, remediation, and validation flow across CloudTrail, CloudWatch, SNS, Lambda, and IAM.

## Folder Structure

```text
screenshots/
├── 01-create-user-alert/
├── 02-create-access-key-alert/
├── 03-admin-policy-alert/
└── README.md
1. CreateUserAlert

Path:

screenshots/01-create-user-alert/

Main proof files:

01-before-user-exists.png — IAM user visible before remediation
02-alarm-in-alarm.png — CloudWatch alarm in ALARM
03-email-user-deleted.png — SNS email notification confirming remediation
04-after-user-gone.png — IAM user removed after remediation

Optional support files:

00-create-user-form.png — user creation form
05-alarm-reset-insufficient-data.png — alarm returned to normal state
2. CreateAccessKeyAlert

Path:

screenshots/02-create-access-key-alert/

Main proof files:

01-key-active.png — access key visible as active
02-alarm-in-alarm.png — CloudWatch alarm in ALARM
03-email-key-disabled.png — SNS email notification confirming remediation
04-after-key-inactive.png — access key shown as inactive after remediation

Optional support files:

00-key-created-page.png — access key creation/retrieval page
05-alarm-reset-insufficient-data.png — alarm returned to normal state
3. AdminPolicyAlert

Path:

screenshots/03-admin-policy-alert/

Main proof files:

01-policy-attached.png — AdministratorAccess attached before remediation
02-alarm-in-alarm.png — CloudWatch alarm in ALARM
03-email-policy-detached.png — SNS email notification confirming remediation
04-after-policy-removed.png — policy removed after remediation

Optional support files:

00-policy-selection.png — policy selection/setup page
05-alarm-reset-insufficient-data.png — alarm returned to normal state
Purpose

These screenshots provide visual proof that the lab was not only configured, but successfully tested end-to-end.

They are intended to demonstrate:

CloudTrail-backed IAM event detection
CloudWatch alarm generation
SNS alert routing
Lambda-based remediation
final remediation outcomes in IAM
end-to-end workflow validation
Notes
Prefer screenshots that show successful remediation outcomes, not only setup pages.
Blur sensitive details such as account IDs, email addresses, ARNs, and access key IDs before upload.
Use clear filenames so each screenshot is easy to map to a specific step in the workflow.
