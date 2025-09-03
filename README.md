# Homebase

Centralized academic workflow automation — assignments from everywhere, in one reliable hub.

# Overview

Homebase is a CLI-based productivity and workflow system that consolidates academic tasks from multiple platforms (Canvas, PrairieLearn, SmartPhysics, Moodle LTI, etc.) into a single hub. The goal is to ensure no assignment slips through the cracks by automatically collecting tasks and generating structured daily/weekly checklists inside Obsidian.

# Features (Current)

✅ CLI application (homebase) with commands: init, doctor, demo, update

✅ Unified task schema (Pydantic model) for consistent representation across sources

✅ Obsidian Markdown templates for daily and master logs

✅ Jinja2 renderer that outputs checklists into your vault

✅ Relative due date formatting (“due today”, “due in 3 days”, “overdue by 2 hr”)

✅ Stable assignment IDs (SHA1 fingerprints) to support rollover

# Roadmap

 Phase 1: CLI tool, JSON schema, Obsidian integration

 Phase 2: Source integrations (Canvas/Moodle LTI, PrairieLearn, SmartPhysics)

 Phase 3: Calendar sync + priority system

 Phase 4: Advanced scheduling & AI-driven study planner

# Tech Stack

Language: Python 3.11+

CLI: Typer

Validation: Pydantic

Templating: Jinja2

Config: python-dotenv

Timezone Handling: zoneinfo (stdlib)

# Project Structure
homebase/
  homebase/
    __init__.py
    cli.py              # CLI commands (init, doctor, demo, update)
    config.py           # Loads .env (vault path, timezone, output dirs)
    models.py           # Assignment schema (Pydantic)
    renderers/
      __init__.py
      obsidian.py       # Renders Markdown from templates
    utils/
      __init__.py
      fingerprint.py    # Stable assignment ID generator
      timefmt.py        # Relative due date + timezone helpers
  templates/
    daily.md.j2         # Daily note layout
    master.md.j2        # Master log layout
  .env.example          # Example config file
  pyproject.toml        # Dependencies + entry point
  README.md

# Installation

Make sure you have Python 3.11+ installed.

# Clone the repository
git clone https://github.com/Adrianv0512/homebase.git
cd homebase

# Create a virtual environment
python -m venv .venv
# Activate venv
source .venv/bin/activate        # mac/linux
.venv\Scripts\activate.ps1       # windows powershell

# Install dependencies in editable mode
pip install -e .


Test the install:

homebase --help


You should see available commands.

First Run

Initialize Homebase with your vault path:

homebase init


Example values:

Vault path: C:/Users/adria/Documents/Obsidian/Vault

Timezone: America/Chicago (or your IANA tz name)

Validate configuration:

homebase doctor


Generate demo notes:

homebase demo


This creates:

Assignments/Daily/YYYY-MM-DD.md

Assignments/Master.md

inside your Obsidian vault.

Open Obsidian and check your new notes 🎉

Next Steps

Implement real source integrations (Canvas, PrairieLearn, etc.) inside homebase/sources/.

Add rollover logic for unfinished tasks.

Extend CLI with filters and weekly summaries.