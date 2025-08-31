# Tetris Cognition — Game & iMotions (WIP)

Custom **Tetris (pygame)** prototype + **iMotions** study materials used in a cognitive-load research setup.  
This repository is part of my ICT studies & research portfolio.

## Repository structure
- **`tetris/`** — pygame project (menu, levels, assets). Entry: `python tetris/main.py`
- **`iMotions/`** — study plan & export tips
- **`documentation/`** — detailed game protocol & log format → see [`game_protocol.md`](documentation/game_protocol.md)
- **`research_log/`** — weekly reports & figures

## Quickstart
```bash
python -m venv .venv
# Windows
. .venv/Scripts/activate
pip install -r requirements.txt
python tetris/main.py
