import hashlib

def make_assignment_id(
    platform: str,
    course_id: str,
    title: str,
    due_at_iso: str | None,
    external_id: str | None = None,
) -> str:
    """
    Generate a stable SHA1 fingerprint for an assignment.

    Components used:
    - platform (e.g., canvas, prairielearn)
    - course_id (e.g., CS225-F25)
    - external_id (if available from the source system)
    - title (assignment name)
    - due_at_iso (ISO 8601 string of due datetime, if available)

    This ensures uniqueness across different platforms and avoids clashes
    when two systems both have an assignment called "Homework 1".
    """
    # Normalize None → ""
    parts = [platform or "", course_id or "", external_id or "", title or "", due_at_iso or ""]
    raw = "|".join(parts)

    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()
    return "sha1:" + digest
