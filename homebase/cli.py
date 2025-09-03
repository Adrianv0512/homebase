from __future__ import annotations
import typer
from pathlib import Path
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from .config import load_config, HomebaseConfig
from .models import Assignment
from .renderers.obsidian import render_daily, render_master
from .utils.fingerprint import make_assignment_id
from .utils.timefmt import get_tz, validate_timezone 

app = typer.Typer(help="Homebase CLI — aggregate assignments into Obsidian")

# ------------------ Commands ------------------

@app.command()
def init(
    vault_path: Path = typer.Option(..., prompt=True, help="Path to your Obsidian vault"),
    tz: str = typer.Option("America/Chicago", help="IANA timezone (e.g., America/Chicago)"),
    daily_dir: str = typer.Option("Assignments/Daily"),
    master_file: str = typer.Option("Assignments/Master.md"),
):
    """
    Initialize Homebase by creating a .env file with basic configuration.
    """
    env_path = Path(".env")
    if env_path.exists():
        typer.confirm(".env already exists — overwrite?", abort=True)

    env_text = (
        f"HOMEBASE_VAULT_PATH={vault_path}\n"
        f"HOMEBASE_TZ={tz}\n"
        f"HOMEBASE_DAILY_DIR={daily_dir}\n"
        f"HOMEBASE_MASTER_FILE={master_file}\n"
    )
    env_path.write_text(env_text, encoding="utf-8")
    typer.secho("Created .env. Run `homebase doctor` to validate.", fg=typer.colors.GREEN)

@app.command()
def doctor():
    """
    Validate configuration and output paths, including timezone availability.
    """
    try:
        cfg = load_config()
    except Exception as e:
        typer.secho(f"Config error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(f"Vault: {cfg.vault_path}")
    typer.echo(f"Timezone: {cfg.timezone}")
    typer.echo(f"Daily dir: {cfg.output_daily_dir}")
    typer.echo(f"Master file: {cfg.output_master_file}")

    if not cfg.vault_path.exists():
        typer.secho("Vault path does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # NEW: check timezone is resolvable (will hint to install tzdata on Windows)
    try:
        validate_timezone(cfg.timezone)
    except RuntimeError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho("Configuration looks good ✅", fg=typer.colors.GREEN)

@app.command()
def demo():
    """
    Generate demo Daily and Master notes using fake assignments.
    """
    cfg = load_config()
    items = _demo_assignments(cfg)
    now = datetime.now(timezone.utc)

    daily_path = render_daily(cfg.vault_path, cfg.output_daily_dir, cfg.timezone, now, items)
    master_path = render_master(cfg.vault_path, cfg.output_master_file, cfg.timezone, now, items)

    typer.secho(f"Wrote: {daily_path}", fg=typer.colors.GREEN)
    typer.secho(f"Wrote: {master_path}", fg=typer.colors.GREEN)

@app.command()
def update():
    """
    Fetch assignments from sources (Canvas, PrairieLearn, etc.).
    Currently a stub — will be implemented in Phase 2.
    """
    cfg = load_config()
    items: list[Assignment] = []

    # TODO: add real source fetchers here
    # items += fetch_canvas(...)
    # items += fetch_prairielearn(...)
    # items += fetch_prairietest(...)
    # items += fetch_smartphysics(...)

    if not items:
        typer.secho("No items fetched (sources not implemented yet). Try `homebase demo`.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=0)

    now = datetime.now(timezone.utc)
    daily_path = render_daily(cfg.vault_path, cfg.output_daily_dir, cfg.timezone, now, items)
    master_path = render_master(cfg.vault_path, cfg.output_master_file, cfg.timezone, now, items)

    typer.secho(f"Updated: {daily_path}", fg=typer.colors.GREEN)
    typer.secho(f"Updated: {master_path}", fg=typer.colors.GREEN)

# ------------------ Helpers ------------------

def _demo_assignments(cfg: HomebaseConfig) -> list[Assignment]:
    tz = get_tz(cfg.timezone)  # <-- use safe wrapper
    now = datetime.now(tz=tz)

    def make(platform, course_id, course_name, title, days_from_now, external_id=None):
        due = (now.replace(hour=23, minute=59, second=0, microsecond=0)
               + timedelta(days=days_from_now))
        aid = make_assignment_id(platform, course_id, title, due.isoformat(), external_id)
        return Assignment(
            id=aid,
            platform=platform,
            course_id=course_id,
            course_name=course_name,
            external_id=external_id,
            title=title,
            due_at=due,
            url=None,
        )

    return [
        make("canvas", "CS225-F25", "CS 225", "MP1: Linked List", 0, "12345"),
        make("smartphysics", "PHYS211-F25", "PHYS 211", "Homework 3", 0, None),
        make("prairietest", "CS173-F25", "CS 173", "Examlet 2", 2, "E2"),
        make("prairielearn", "CS225-F25", "CS 225", "Quiz 1", 3, "Q1"),
        make("canvas", "MATH241-F25", "Math 241", "Homework 4", 5, "HW4"),
    ]