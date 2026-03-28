# Architecture

## Final Working Flow

```text
IAM action occurs
→ CloudTrail records the event
→ CloudWatch Logs receives the CloudTrail log entry
→ Metric filter matches the event
→ CloudWatch alarm enters ALARM state
→ SNS topic (SecurityAlerts-Lambda) sends the alarm to Lambda
→ Lambda looks up the matching CloudTrail event
→ Lambda performs IAM remediation
→ Lambda publishes a result notification to SNS topic (SecurityAlerts-Email)
→ Outlook email receives the remediation result

## Services and Roles

### AWS IAM
Source of the risky actions being tested.

### AWS CloudTrail
Records IAM activity for detection and event lookup.

### AWS CloudWatch Logs / Metric Filters
Detect specific IAM event patterns from CloudTrail logs.

### AWS CloudWatch Alarms
Trigger when suspicious IAM activity is detected.

### AWS SNS
- `SecurityAlerts-Lambda` → delivers CloudWatch alarm notifications to Lambda
- `SecurityAlerts-Email` → sends remediation result emails

### AWS Lambda (`SOC_AutoRemediate`)
Looks up recent CloudTrail events and performs remediation actions.

## Remediation Mapping

### CreateUserAlert
Deletes the newly created IAM user.

### CreateAccessKeyAlert
Disables the newest active access key.

### AdminPolicyAlert
Detaches `AdministratorAccess` from the targeted user.

## Security Improvements Added

- region-aware CloudTrail lookup using `CLOUDTRAIL_REGION`
- protected username safeguard using `PROTECTED_USERS`
- separated SNS topics to prevent Lambda from parsing its own notification messages
- improved logging for event lookup and remediation results
