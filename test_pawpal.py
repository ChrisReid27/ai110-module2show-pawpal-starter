import pytest

from pawpal_system import Pet, Task

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
