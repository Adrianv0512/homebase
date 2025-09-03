from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..models import Assignment
from ..utils.timefmt import relative_due, to_zone

env = Environment(
    loader=FileSystemLoader(str(Path(__file__).resolve().parents[2] / "templates")),
    autoescape=select_autoescape(enabled_extensions=("html", "xml"))
)

def _month_key(dt: datetime, tz: str) -> str:
    local = to_zone(dt, tz)
    return local.strftime("%B %Y")

def render_daily(
    vault: Path,
    daily_dir: str,
    tz: str,
    today: datetime,
    items: List[Assignment],
) -> Path:
    today_local = to_zone(today, tz)
    date_slug = today_local.strftime("%Y-%m-%d")

    out_dir = vault / daily_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{date_slug}.md"

    due_today, upcoming = [], []
    for a in items:
        rel = relative_due(today, a.due_at, tz)
        view = {**a.model_dump(), "relative_due": rel}
        if a.due_at:
            due_local = to_zone(a.due_at, tz)
            delta_days = (due_local.date() - today_local.date()).days
            if delta_days == 0:
                due_today.append(view)
            elif 0 < delta_days <= 7:
                upcoming.append(view)
        else:
            upcoming.append(view)

    tpl = env.get_template("daily.md.j2")
    md = tpl.render(today_date=date_slug, due_today=due_today, upcoming=upcoming)
    out_path.write_text(md, encoding="utf-8")
    return out_path

def render_master(
    vault: Path,
    master_file: str,
    tz: str,
    now: datetime,
    items: List[Assignment],
) -> Path:
    out_path = vault / master_file
    out_path.parent.mkdir(parents=True, exist_ok=True)

    by_month: Dict[str, list] = {}
    for a in items:
        due = a.due_at or now
        key = _month_key(due, tz)
        rel = relative_due(now, a.due_at, tz)
        view = {**a.model_dump(), "relative_due": rel}
        by_month.setdefault(key, []).append(view)

    tpl = env.get_template("master.md.j2")
    md = tpl.render(by_month=by_month)
    out_path.write_text(md, encoding="utf-8")
    return out_path
