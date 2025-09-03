from __future__ import annotations
from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Optional
from datetime import datetime, timezone  # <-- timezone added

Platform = Literal["canvas", "prairielearn", "prairietest", "smartphysics", "moodle"]
Kind = Literal["assignment", "quiz", "exam", "lab", "project", "homework", "other"]
Status = Literal["pending", "completed", "cancelled", "ignored"]

class Assignment(BaseModel):
    # Identifiers
    id: str = Field(..., description="Stable fingerprint for deduplication")
    platform: Platform
    course_id: str
    course_name: str
    external_id: Optional[str] = None

    # Content
    title: str
    kind: Kind = "assignment"
    description: Optional[str] = None

    # Dates (timezone-aware)
    due_at: Optional[datetime] = None
    available_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Links
    url: Optional[HttpUrl] = None
    source_path: Optional[str] = None

    # Status / metadata
    status: Status = "pending"
    points_possible: Optional[float] = None
    weight: Optional[float] = None

    # System metadata (timezone-aware UTC)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1
