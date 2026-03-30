# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

PawPal+ goes beyond a simple task list with four algorithmic features:

- **Sort by time** — `DayScheduler.sort_by_time()` uses `sorted()` with a lambda key on `HH:MM` strings to return tasks in chronological order regardless of the order they were added.
- **Filter tasks** — `DayScheduler.filter_tasks(status, category)` lets you slice the task list by completion status (`pending` / `complete`) or by category (e.g. `feeding`, `walk`).
- **Recurring tasks** — `CareTask` supports a `frequency` field (`once` / `daily` / `weekly`). When `DayScheduler.complete_task()` marks a task done, it calls `next_occurrence()` which uses Python's `timedelta` to calculate the next due date and automatically appends a fresh copy of the task.
- **Conflict detection** — `DayScheduler.detect_conflicts()` compares every pair of scheduled tasks to check whether their time windows overlap. It returns human-readable warning strings instead of crashing, so the owner can decide how to resolve them.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
