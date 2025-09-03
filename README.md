# Homebase

Centralized academic workflow automation — assignments from everywhere, in one reliable hub.

## Overview
Homebase is a personal productivity and workflow system that consolidates academic tasks from multiple platforms (Canvas, PrairieLearn, SmartPhysics, Moodle LTI, etc.) into a single hub. The goal is to ensure no assignment slips through the cracks by automatically collecting tasks and generating structured daily/weekly checklists.

## Features
- ✅ Scrape/collect assignments from multiple platforms  
- ✅ Unified task representation (JSON schema)  
- ✅ Automatic daily & weekly checklist generation  
- ✅ Integration with Obsidian (templates, master log, rollover tasks)  
- ✅ Optional sync with Google Calendar  

## Roadmap
- [ ] Phase 1: CLI tool & JSON schema  
- [ ] Phase 2: Scraping/Platform integrations (Canvas/Moodle, PrairieLearn, SmartPhysics)  
- [ ] Phase 3: Obsidian + Calendar integration  
- [ ] Phase 4: Advanced scheduling & notifications  

## Tech Stack
- **Backend**: Python (FastAPI / Flask for API endpoints, CLI tool)  
- **Automation**: Selenium, Playwright, BeautifulSoup  
- **Storage**: SQLite or JSON-based logs  
- **Integrations**: Google Calendar API, Obsidian Templater  

## Getting Started
```bash
# Clone the repository
git clone https://github.com/<your-username>/homebase.git

# Enter project folder
cd homebase

# (Setup instructions coming soon)

