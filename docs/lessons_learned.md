# Lessons Learned - AWS IAM Auto Remediation Lab

## Key Takeaways

### 1. IAM is High Risk
IAM actions are some of the most sensitive operations in AWS.

Small changes like attaching policies or creating users can have major security impact.

---

### 2. CloudTrail is Critical for Visibility
CloudTrail provides the foundation for detecting activity in AWS.

Without proper logging, detecting suspicious behavior is extremely difficult.

---

### 3. Detection Requires Proper Filtering
Not all events are important.

Filtering for specific IAM actions is necessary to reduce noise and focus on high-risk behavior.

---

### 4. Alerts vs Automation
There is a major difference between:

- Alerting (SNS, CloudWatch)
- Auto-remediation (Lambda)

Automation must be carefully designed to avoid breaking legitimate workflows.

---

### 5. Permissions Are Everything
IAM roles and policies must be configured correctly.

Even small permission issues can break automation or prevent detection workflows from functioning.

---

### 6. Region Consistency Matters
AWS services must be in the same region to work correctly.

Mismatch between Lambda, CloudWatch, SNS, and EventBridge can cause failures.

---

### 7. Troubleshooting is a Key Skill
A large part of this lab involved:

- Debugging permissions
- Fixing event triggers
- Resolving service misconfigurations

This reflects real-world cloud security work.

---

## What I Would Improve

- Add stricter least-privilege IAM policies
- Improve Lambda logic for safer remediation
- Add logging and error handling
- Implement better alert filtering
- Expand detection coverage

---

## Final Thought
This lab demonstrates how cloud security is not just about tools, but about:

- Understanding how services connect
- Debugging real issues
- Thinking like both an attacker and defender

---

## Challenges Faced

- IAM permission issues prevented Lambda from performing actions correctly.
- Initial alert pipeline issues caused CloudWatch alarms and SNS notifications not to trigger.
- Debugging misconfigurations between CloudTrail, CloudWatch, and SNS required multiple iterations.
- Ensuring alerts were reliably generated before attempting automation logic.

---

-  Learned the importance of validating alert pipelines before implementing remediation logic.
