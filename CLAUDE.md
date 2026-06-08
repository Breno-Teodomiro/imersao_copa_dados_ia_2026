# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A World Cup 2026 bracket pool (bolão) web app built with Python and Streamlit. Portfolio project — keep the architecture simple.

## Stack

- **Frontend/UI**: Streamlit
- **Database**: to be decided (SQLite for simplicity, or a cloud option like Supabase)
- **Language**: Python

## Core Features (from escopo.md)

1. **Participant registration**: name, phone, email
2. **Group stage picks**: user selects 1st and 2nd place for each of the 8 groups (Groups A–H)
3. **Best third-place teams**: the 4 best third-place qualifiers are chosen randomly (to simplify logic)
4. **Data persistence**: all picks saved to a database

## Design Reference

The UI should follow the layout in `picture/tela_de_captura.png` — a "Simulador da Copa do Mundo 2026" style page showing all groups (A through I/J) with team flags and match results grid per group.

## Development Commands

```bash
# Install dependencies
pip install streamlit

# Run the app
streamlit run app.py
```

## Architecture Notes

- Keep it single-file (`app.py`) or a minimal multi-file layout (`app.py` + `db.py`) — no overengineering
- Group stage: 8 groups × 4 teams each; user picks positions 1 and 2 per group
- The 8 best third-place teams are randomly assigned from the pool of 3rd-place finishers
- Store each submission as one row per participant with their picks serialized (JSON column or normalized table)
