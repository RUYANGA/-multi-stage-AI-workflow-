"""
email_validator module
Generated from spec.json (chat stage) and integrated by the IDE-stage assistant.
"""

DISPOSABLE_DOMAINS = {"mailinator.com", "tempmail.com"}


def validate_email(email: str) -> dict:
    """Validate an email address per business rules in spec.json.

    Returns:
        dict: {"is_valid": bool, "reason": str | None}
    """
    if email.count("@") != 1:
        return {"is_valid": False, "reason": "must contain exactly one '@'"}

    local, domain = email.split("@")

    if not (1 <= len(local) <= 64):
        return {"is_valid": False, "reason": "local part must be 1-64 characters"}

    if "." not in domain:
        return {"is_valid": False, "reason": "domain must contain at least one '.'"}

    if domain.startswith((".", "-")) or domain.endswith((".", "-")):
        return {"is_valid": False, "reason": "domain must not start/end with '.' or '-'"}

    if domain.lower() in DISPOSABLE_DOMAINS:
        return {"is_valid": False, "reason": "disposable email domains are not allowed"}

    return {"is_valid": True, "reason": None}
