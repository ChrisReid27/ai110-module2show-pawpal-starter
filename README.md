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

## Smarter Scheduling

The scheduling system now includes lightweight algorithms to make daily plans more useful without adding heavy complexity.

- Time-first ordering: tasks with `start_time_minutes` are sorted ahead of untimed tasks, with priority and duration used as tie-breakers.
- Filtering helpers: `Scheduler.filter_tasks(...)` supports filtering by pet, status, and type for quick views in the UI or CLI.
- Recurring tasks: tasks can be marked as `daily`, `weekly`, or use a `recurrence_interval_days` rule. Due checks are based on `last_completed_date`.
- Conflict warnings: `Scheduler.detect_time_conflicts(...)` reports tasks that share the same start time without crashing the program.
- Recurrence on completion: when a daily or weekly task is marked complete, a new instance is created for the next due date.

## Testing PawPal+


What to validate in tests:

- Task completion and recurrence behavior (daily/weekly/interval rules)
- Sorting by time, priority, and duration tie-breakers
- Conflict detection when two tasks share the same start time
- Empty states (pets with no tasks, owners with no pets)

Command to run tests:

```bash
python -m pytest
```

If a test fails, read the assertion message first, then confirm the related method behavior in pawpal_system.py and update either the code or the test to match the intended rule.

Confidence Level: 4 to 5 stars.


## Features

- Time-first sorting: tasks with `start_time_minutes` come first, then priority, duration, and title.
- Preference-aware scoring: boosts preferred task types/tags and special-needs tasks.
- Conflict warnings: detects tasks that share a start time and surfaces warnings.
- Dependency handling: skips tasks until required `depends_on` tasks are scheduled.
- Due-date filtering: honors `daily`, `weekly`, and interval recurrence rules via `last_completed_date`.
- Recurrence on completion: daily/weekly tasks spawn the next instance when marked complete.

Demo:
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)