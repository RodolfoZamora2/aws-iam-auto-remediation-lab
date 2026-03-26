import os
import json
import time
import datetime
import boto3
from botocore.exceptions import ClientError

# AWS clients
iam = boto3.client("iam")
sns = boto3.client("sns")
ct = boto3.client("cloudtrail")

# ---- Config ----
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
ADMIN_POLICY_ARN = "arn:aws:iam::aws:policy/AdministratorAccess"

# Lookup timing
LOOKUP_RETRIES = 6
LOOKUP_SLEEP_SECONDS = 10
LOOKUP_WINDOW_MINUTES = 60


# ---------- Helpers ----------
def _log(msg: str):
    print(msg)


def _publish(subject: str, msg: str):
    _log(f"[NOTIFY] {subject}: {msg}")
    if SNS_TOPIC_ARN:
        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=subject[:100],
                Message=msg[:3000]
            )
        except Exception as e:
            _log(f"[ERROR] SNS publish failed: {e}")


def _extract_alarm_name(event):
    try:
        record = event["Records"][0]
        sns_message_raw = record["Sns"]["Message"]
        _log(f"[DEBUG] Raw SNS message: {str(sns_message_raw)[:1000]}")

        sns_message = json.loads(sns_message_raw)
        if isinstance(sns_message, dict):
            return sns_message.get("AlarmName")

        return None
    except Exception as e:
        _log(f"[ERROR] Failed to extract alarm name: {e}")
        return None


def _lookup_latest(event_name: str, minutes: int = LOOKUP_WINDOW_MINUTES):
    for attempt in range(1, LOOKUP_RETRIES + 1):
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(minutes=minutes)

        try:
            resp = ct.lookup_events(
                LookupAttributes=[
                    {"AttributeKey": "EventName", "AttributeValue": event_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                MaxResults=20,
            )
        except ClientError as e:
            _log(f"[ERROR] CloudTrail lookup failed for {event_name}: {e}")
            time.sleep(LOOKUP_SLEEP_SECONDS)
            continue

        events = resp.get("Events", [])
        if events:
            latest = sorted(events, key=lambda e: e["EventTime"], reverse=True)[0]
            try:
                parsed = json.loads(latest["CloudTrailEvent"])
                _log(f"[INFO] Found {event_name} event on attempt {attempt}")
                return parsed
            except Exception as e:
                _log(f"[ERROR] Failed parsing CloudTrailEvent JSON: {e}")
                return None

        _log(f"[INFO] No {event_name} event yet on attempt {attempt}, waiting...")
        time.sleep(LOOKUP_SLEEP_SECONDS)

    return None


def _disable_newest_active_key(user_name: str):
    results = []
    try:
        keys = iam.list_access_keys(UserName=user_name).get("AccessKeyMetadata", [])
        keys = sorted(keys, key=lambda k: k["CreateDate"], reverse=True)

        for key in keys:
            if key["Status"] == "Active":
                iam.update_access_key(
                    UserName=user_name,
                    AccessKeyId=key["AccessKeyId"],
                    Status="Inactive"
                )
                results.append(f"Disabled access key {key['AccessKeyId']} for {user_name}")
                break

        if not results:
            results.append(f"No active keys found for {user_name}")

    except Exception as e:
        results.append(f"Failed to disable access key for {user_name}: {e}")

    return results


def _detach_admin_policy(user_name: str):
    results = []
    try:
        policies = iam.list_attached_user_policies(UserName=user_name).get("AttachedPolicies", [])
        detached = False

        for policy in policies:
            if (
                policy.get("PolicyArn") == ADMIN_POLICY_ARN
                or policy.get("PolicyName") == "AdministratorAccess"
            ):
                iam.detach_user_policy(
                    UserName=user_name,
                    PolicyArn=policy["PolicyArn"]
                )
                results.append(f"Detached AdministratorAccess from {user_name}")
                detached = True

        if not detached:
            results.append(f"AdministratorAccess not attached to {user_name}")

    except Exception as e:
        results.append(f"Failed to detach AdministratorAccess from {user_name}: {e}")

    return results


def _delete_user(user_name: str):
    results = []
    try:
        # If user has keys, login profile, policies, etc. delete_user can fail.
        # This keeps it simple for your lab if it's just a new plain user.
        iam.delete_user(UserName=user_name)
        results.append(f"Deleted newly created user {user_name}")
    except Exception as e:
        results.append(f"Failed to delete user {user_name}: {e}")

    return results


# ---------- Handler ----------
def lambda_handler(event, context):
    _log("[DEBUG] Incoming event received")

    alarm_name = _extract_alarm_name(event)
    if not alarm_name:
        return {"status": "error", "reason": "alarm_name_not_found"}

    _log(f"[INFO] Alarm received: {alarm_name}")

    # -------- Scenario 1: CreateAccessKeyAlert --------
    if "AccessKey" in alarm_name:
        evt = _lookup_latest("CreateAccessKey")
        if not evt:
            _publish("SOC AutoRemediate", "No recent CreateAccessKey event found after retries.")
            return {"status": "ok", "action": "none"}

        request_params = evt.get("requestParameters", {}) or {}
        user_identity = evt.get("userIdentity", {}) or {}

        user_name = request_params.get("userName") or user_identity.get("userName")
        if not user_name:
            _publish("SOC AutoRemediate", "CreateAccessKey detected but no userName found.")
            return {"status": "ok", "action": "none"}

        results = _disable_newest_active_key(user_name)
        _publish("SOC AutoRemediate - Key Disabled", "\n".join(results))
        return {"status": "ok", "action": "disable_key", "user": user_name}

    # -------- Scenario 2: AdminPolicyAlert --------
    if "AdminPolicy" in alarm_name or "AttachAdminPolicy" in alarm_name:
        evt = _lookup_latest("AttachUserPolicy")
        if not evt:
            _publish("SOC AutoRemediate", "No recent AttachUserPolicy event found after retries.")
            return {"status": "ok", "action": "none"}

        request_params = evt.get("requestParameters", {}) or {}
        user_identity = evt.get("userIdentity", {}) or {}

        policy_arn = request_params.get("policyArn")
        user_name = request_params.get("userName") or user_identity.get("userName")

        if policy_arn != ADMIN_POLICY_ARN:
            _publish("SOC AutoRemediate", f"Attached policy was not AdministratorAccess: {policy_arn}")
            return {"status": "ok", "action": "none"}

        if not user_name:
            _publish("SOC AutoRemediate", "Admin policy attach detected but no userName found.")
            return {"status": "ok", "action": "none"}

        results = _detach_admin_policy(user_name)
        _publish("SOC AutoRemediate - Admin Detached", "\n".join(results))
        return {"status": "ok", "action": "detach_admin", "user": user_name}

    # -------- Scenario 3: CreateUserAlert --------
    if "CreateUser" in alarm_name:
        evt = _lookup_latest("CreateUser")
        if not evt:
            _publish("SOC AutoRemediate", "No recent CreateUser event found after retries.")
            return {"status": "ok", "action": "none"}

        request_params = evt.get("requestParameters", {}) or {}
        user_name = request_params.get("userName")

        if not user_name:
            _publish("SOC AutoRemediate", "CreateUser detected but no created userName found.")
            return {"status": "ok", "action": "none"}

        results = _delete_user(user_name)
        _publish("SOC AutoRemediate - User Deleted", "\n".join(results))
        return {"status": "ok", "action": "delete_user", "user": user_name}

    _log(f"[INFO] Unhandled alarm name: {alarm_name}")
    return {"status": "ok", "action": "unhandled_alarm", "alarm_name": alarm_name}
