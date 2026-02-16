from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, PetInfo, Schedule, Scheduler, Task, UserInfo

def test_task_mark_completed_updates_status() -> None:
	task = Task(
		task_id="t1",
		title="Feed",
		duration_minutes=5,
		priority="low",
		task_type="care",
	)

	assert task.completed is False
	task.mark_completed()
	assert task.completed is True


def test_pet_add_task_increases_count() -> None:
	pet = Pet(name="Milo", species="cat", age=3)
	task = Task(
		task_id="t2",
		title="Brush",
		duration_minutes=10,
		priority="medium",
		task_type="grooming",
	)

	assert len(pet.tasks) == 0
	pet.add_task(task)
	assert len(pet.tasks) == 1


def test_pet_with_no_tasks_returns_empty_lists() -> None:
	pet = Pet(name="Nala", species="dog", age=2)

	assert pet.get_tasks() == []
	assert pet.get_pending_tasks() == []


def test_task_is_due_on_once_completed_returns_false() -> None:
	task = Task(
		task_id="t3",
		title="Vet visit",
		duration_minutes=30,
		priority="high",
		task_type="care",
		frequency="once",
	)

	task.mark_completed()
	assert task.is_due_on(date.today()) is False


def test_task_is_due_on_daily_after_one_day_returns_true() -> None:
	task = Task(
		task_id="t4",
		title="Walk",
		duration_minutes=20,
		priority="medium",
		task_type="exercise",
		frequency="daily",
	)

	today = date.today()
	task.last_completed_date = today - timedelta(days=1)
	assert task.is_due_on(today) is True


def test_schedule_orders_same_time_by_title() -> None:
	owner = UserInfo(name="Sam", available_time_minutes=60)
	pet = PetInfo(name="Milo", species="cat", age=3)
	task_b = Task(
		task_id="t5",
		title="Brush",
		duration_minutes=10,
		priority="low",
		task_type="grooming",
		start_time_minutes=480,
	)
	task_a = Task(
		task_id="t6",
		title="Apply ointment",
		duration_minutes=10,
		priority="low",
		task_type="care",
		start_time_minutes=480,
	)

	schedule = Schedule(
		date=date.today(),
		owner=owner,
		pet=pet,
		available_tasks=[task_b, task_a],
	)

	schedule.generate_schedule()
	scheduled_titles = [task.title for task in schedule.get_scheduled_tasks()]
	assert scheduled_titles == ["Apply ointment"]


def test_scheduler_detects_conflict_at_same_start_time() -> None:
	owner = Owner(name="Chris")
	pet_one = Pet(name="Milo", species="cat", age=3)
	pet_two = Pet(name="Rex", species="dog", age=5)

	pet_one.add_task(
		Task(
			task_id="t7",
			title="Feed",
			duration_minutes=5,
			priority="low",
			task_type="care",
			start_time_minutes=480,
		)
	)
	pet_two.add_task(
		Task(
			task_id="t8",
			title="Walk",
			duration_minutes=15,
			priority="medium",
			task_type="exercise",
			start_time_minutes=480,
		)
	)

	owner.add_pet(pet_one)
	owner.add_pet(pet_two)

	scheduler = Scheduler(owner)
	warnings = scheduler.detect_time_conflicts()

	assert len(warnings) == 1
	assert "08:00" in warnings[0]
