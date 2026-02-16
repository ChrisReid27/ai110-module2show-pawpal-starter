"""

This module provides a comprehensive system for managing pet care tasks and scheduling.
It includes classes for representing pet owners, pets, individual tasks, and generating
optimized daily schedules based on time constraints and preferences.

Classes:
    UserInfo: Represents a pet owner with time constraints and preferences.
    PetInfo: Stores static pet information and special needs.
    Task: Represents individual pet care tasks with scheduling properties.
    Schedule: Generates and manages daily pet care schedules.
    Pet: Manages a pet and its associated tasks.
    Owner: Manages multiple pets and their tasks.
    Scheduler: Retrieves, organizes, and manages tasks across all pets.
PawPal+ System Classes
Pet care task scheduling and management system.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass
class UserInfo:
    """Represents the pet owner with time constraints and preferences."""
    name: str
    available_time_minutes: int
    preferences: Dict = field(default_factory=dict)

    def get_available_time(self) -> int:
        """Returns the owner's available time in minutes."""
        return self.available_time_minutes

    def set_preferences(self, preferences: Dict) -> None:
        """Updates the owner's preferences."""
        self.preferences = dict(preferences)

    def get_name(self) -> str:
        """Returns the owner's name."""
        return self.name


@dataclass
class PetInfo:
    """Stores pet information and special needs."""
    name: str
    species: str
    age: int = 0
    special_needs: List[str] = field(default_factory=list)

    def get_pet_info(self) -> Dict:
        """Returns all pet information as a dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "special_needs": list(self.special_needs),
        }

    def has_special_needs(self) -> bool:
        """Checks if the pet has any special needs."""
        return bool(self.special_needs)

    def get_name(self) -> str:
        """Returns the pet's name."""
        return self.name


@dataclass
class Task:
    """Represents individual pet care tasks."""
    task_id: str
    title: str
    duration_minutes: int
    priority: str
    task_type: str
    completed: bool = False
    description: str = ""
    frequency: str = "once"
    start_time_minutes: Optional[int] = None
    recurrence_interval_days: Optional[int] = None
    last_completed_date: Optional[date] = None
    applicable_species: List[str] = field(default_factory=list)
    preference_tags: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    requires_special_needs: bool = False

    def __post_init__(self) -> None:
        """Ensures tasks have a description by defaulting to the title."""
        if not self.description:
            self.description = self.title

    def mark_completed(self) -> None:
        """Marks the task as completed."""
        self.completed = True
        self.last_completed_date = date.today()

    def get_priority_value(self) -> int:
        """Returns numeric priority value (high=3, medium=2, low=1)."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority.lower().strip(), 0)

    def is_completed(self) -> bool:
        """Returns the completion status of the task."""
        return self.completed

    def is_due_on(self, target_date: date) -> bool:
        """Returns True if the task is due on the target date."""
        if self.completed and self.frequency == "once":
            return False
        frequency = (self.frequency or "once").lower().strip()
        if frequency == "once":
            return True
        if self.recurrence_interval_days:
            if not self.last_completed_date:
                return True
            return (target_date - self.last_completed_date).days >= self.recurrence_interval_days
        if frequency == "daily":
            if not self.last_completed_date:
                return True
            return (target_date - self.last_completed_date).days >= 1
        if frequency == "weekly":
            if not self.last_completed_date:
                return True
            return (target_date - self.last_completed_date).days >= 7
        return True

    def __str__(self) -> str:
        """Returns a string representation of the task."""
        status = "done" if self.completed else "pending"
        return (
            f"{self.task_id}: {self.description} ({self.duration_minutes} min, "
            f"{self.frequency}, {status})"
        )


class Schedule:
    """Generates and manages the daily pet care schedule."""

    def __init__(
        self,
        date: datetime,
        owner: UserInfo,
        pet: PetInfo,
        available_tasks: List[Task]
    ):
        """Initializes a schedule for a given date, owner, pet, and task list."""
        self.date = date
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks
        self.scheduled_tasks: List[Task] = []
        self.total_time_minutes = 0
        self.explanation = ""
        self.conflicts: List[Tuple[Task, Task]] = []

    def generate_schedule(self) -> None:
        """Creates an optimized schedule based on constraints."""
        self.scheduled_tasks = []
        self.total_time_minutes = 0
        self.explanation = ""
        self.conflicts = []

        available_time = self.owner.get_available_time()
        preferences = self.owner.preferences or {}
        preferred_types = set(preferences.get("preferred_task_types", []))
        avoid_types = set(preferences.get("avoid_task_types", []))
        preferred_tags = set(preferences.get("preferred_tags", []))
        avoid_tags = set(preferences.get("avoid_tags", []))
        max_tasks = preferences.get("max_tasks")
        prioritize_short = bool(preferences.get("prioritize_short_tasks", False))

        excluded = []
        candidates = []
        for task in self.available_tasks:
            if task.is_completed():
                excluded.append((task, "already completed"))
                continue
            if not task.is_due_on(self.date.date()):
                excluded.append((task, "not due today"))
                continue
            if not self._task_matches_pet(task):
                excluded.append((task, "not applicable to pet"))
                continue
            if task.task_type in avoid_types:
                excluded.append((task, "owner avoids task type"))
                continue
            if avoid_tags and set(task.preference_tags) & avoid_tags:
                excluded.append((task, "owner avoids task tags"))
                continue
            candidates.append(task)

        def sort_key(task: Task) -> tuple:
            """
            Generate a sorting key for a task based on multiple prioritization criteria.
            
            This function creates a tuple used to sort tasks by:
            1. Start time (earlier times first; tasks without start times ranked lowest)
            2. Priority score (higher scores first, with bonuses for preferred types, tags, and special needs)
            3. Duration (shorter tasks first if prioritize_short is True)
            4. Title (alphabetical order as a tiebreaker)
            
            Args:
                task (Task): The task to generate a sort key for.
            
            Returns:
                tuple: A sorting key containing (time_key, negative_score, duration, title_lower)
                    - time_key (int): Start time in minutes, or 10^9 if not set
                    - negative_score (int): Negative priority value to sort high scores first
                    - duration (int): Task duration in minutes, or 0 if not prioritizing short tasks
                    - title_lower (str): Lowercase task title for alphabetical sorting
            """
            time_key = task.start_time_minutes if task.start_time_minutes is not None else 10**9
            score = task.get_priority_value() * 10
            if task.task_type in preferred_types:
                score += 5
            if preferred_tags and set(task.preference_tags) & preferred_tags:
                score += 4
            if self.pet.has_special_needs() and task.requires_special_needs:
                score += 6
            return (time_key, -score, task.duration_minutes if prioritize_short else 0, task.title.lower())

        remaining = sorted(candidates, key=sort_key)
        scheduled_ids = set()
        explanations = []
        progress = True

        while remaining and progress:
            progress = False
            next_remaining = []
            for task in remaining:
                if not self._dependencies_met(task, scheduled_ids):
                    next_remaining.append(task)
                    continue
                if max_tasks is not None and len(self.scheduled_tasks) >= int(max_tasks):
                    explanations.append("Stopped scheduling due to max_tasks preference.")
                    remaining = []
                    progress = True
                    break
                if self.add_task_to_schedule(task):
                    scheduled_ids.add(task.task_id)
                    explanations.append(f"Scheduled {task.title} based on priority and fit.")
                    progress = True
                else:
                    conflict = self._find_time_conflict(task)
                    if conflict:
                        explanations.append(
                            f"Skipped {task.title}; time conflict with {conflict.title}."
                        )
                    else:
                        explanations.append(f"Skipped {task.title}; not enough time remaining.")
            remaining = next_remaining

        for task, reason in excluded:
            explanations.append(f"Excluded {task.title}: {reason}.")

        for task in remaining:
            if not self._dependencies_met(task, scheduled_ids):
                explanations.append(f"Skipped {task.title}; unmet dependencies.")
            else:
                explanations.append(f"Skipped {task.title}; not enough time remaining.")

        if not self.scheduled_tasks and available_time <= 0:
            explanations.append("No tasks scheduled because available time is zero.")

        self.explanation = "\n".join(explanations).strip()

    def add_task_to_schedule(self, task: Task) -> bool:
        """Adds a task to the schedule if time permits and there is no conflict."""
        if task.duration_minutes <= 0:
            return False
        if (self.total_time_minutes + task.duration_minutes) > self.owner.get_available_time():
            return False
        if self._has_time_conflict(task):
            return False
        self.scheduled_tasks.append(task)
        self.total_time_minutes += task.duration_minutes
        return True

    def validate_schedule(self) -> bool:
        """Checks if the schedule fits within time constraints."""
        total_time = self.calculate_total_time()
        return total_time <= self.owner.get_available_time()

    def get_explanation(self) -> str:
        """Returns the reasoning for the schedule decisions."""
        return self.explanation

    def calculate_total_time(self) -> int:
        """Computes the total time of all scheduled tasks."""
        self.total_time_minutes = sum(task.duration_minutes for task in self.scheduled_tasks)
        return self.total_time_minutes

    def get_scheduled_tasks(self) -> List[Task]:
        """Returns the list of scheduled tasks."""
        return list(self.scheduled_tasks)

    def get_conflicts(self) -> List[Tuple[Task, Task]]:
        """Returns detected time conflicts among scheduled tasks."""
        return list(self.conflicts)

    def _task_matches_pet(self, task: Task) -> bool:
        """Checks whether a task applies to the pet based on species and special needs."""
        if task.applicable_species:
            if self.pet.species.lower() not in {s.lower() for s in task.applicable_species}:
                return False
        if task.requires_special_needs and not self.pet.has_special_needs():
            return False
        return True

    def _has_time_conflict(self, task: Task) -> bool:
        """Returns True if the task overlaps any already scheduled timed task."""
        return self._find_time_conflict(task) is not None

    def _find_time_conflict(self, task: Task) -> Optional[Task]:
        """Finds the first scheduled task that overlaps in time with the given task."""
        if task.start_time_minutes is None:
            return None
        task_end = task.start_time_minutes + max(task.duration_minutes, 0)
        for scheduled in self.scheduled_tasks:
            if scheduled.start_time_minutes is None:
                continue
            scheduled_end = scheduled.start_time_minutes + max(scheduled.duration_minutes, 0)
            if task.start_time_minutes < scheduled_end and scheduled.start_time_minutes < task_end:
                self.conflicts.append((task, scheduled))
                return scheduled
        return None

    @staticmethod
    def _dependencies_met(task: Task, scheduled_ids: set) -> bool:
        """Returns True when all dependency IDs are already scheduled."""
        return all(dep_id in scheduled_ids for dep_id in task.depends_on)


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Removes a task by id. Returns True if removed."""
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks.pop(index)
                return True
        return False

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        """Returns tasks for this pet."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.is_completed()]

    def get_pending_tasks(self) -> List[Task]:
        """Returns incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.is_completed()]


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Removes a pet by name. Returns True if removed."""
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                self.pets.pop(index)
                return True
        return False

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Returns a pet by name, if found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Returns tasks across all pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Returns tasks across all pets."""
        return self.owner.get_all_tasks(include_completed=include_completed)

    def get_tasks_by_pet(self, include_completed: bool = True) -> Dict[str, List[Task]]:
        """Returns tasks grouped by pet name."""
        grouped: Dict[str, List[Task]] = {}
        for pet in self.owner.pets:
            grouped[pet.name] = pet.get_tasks(include_completed=include_completed)
        return grouped

    def get_pending_tasks(self) -> List[Task]:
        """Returns all incomplete tasks across pets."""
        return self.owner.get_all_tasks(include_completed=False)

    def detect_time_conflicts(self, include_completed: bool = False) -> List[str]:
        """Returns warning messages for tasks scheduled at the same time."""
        tasks_by_time: Dict[int, List[Tuple[str, Task]]] = {}
        for pet in self.owner.pets:
            for task in pet.get_tasks(include_completed=include_completed):
                if task.start_time_minutes is None:
                    continue
                tasks_by_time.setdefault(task.start_time_minutes, []).append((pet.name, task))

        warnings: List[str] = []
        for start_time, entries in sorted(tasks_by_time.items()):
            if len(entries) < 2:
                continue
            time_label = f"{start_time // 60:02d}:{start_time % 60:02d}"
            names = ", ".join(
                f"{pet_name} - {task.title}" for pet_name, task in entries
            )
            warnings.append(f"Warning: {time_label} conflict between {names}.")
        return warnings

    def mark_task_completed(self, task_id: str) -> bool:
        """Marks a task complete across all pets. Returns True if found."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.task_id == task_id:
                    task.mark_completed()
                    next_task = self._create_next_recurring_task(task, pet)
                    if next_task:
                        pet.add_task(next_task)
                    return True
        return False

    def _create_next_recurring_task(self, task: Task, pet: Pet) -> Optional[Task]:
        """Creates the next daily or weekly task instance, or returns None for other frequencies."""
        frequency = (task.frequency or "once").lower().strip()
        if frequency not in {"daily", "weekly"}:
            return None
        today = date.today()
        days = 1 if frequency == "daily" else 7
        next_due_date = today + timedelta(days=days)
        next_task_id = self._build_recurring_task_id(task.task_id, next_due_date, pet)
        return Task(
            task_id=next_task_id,
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            task_type=task.task_type,
            completed=False,
            description=task.description,
            frequency=task.frequency,
            start_time_minutes=task.start_time_minutes,
            recurrence_interval_days=task.recurrence_interval_days,
            last_completed_date=today,
            applicable_species=list(task.applicable_species),
            preference_tags=list(task.preference_tags),
            depends_on=list(task.depends_on),
            requires_special_needs=task.requires_special_needs,
        )

    @staticmethod
    def _build_recurring_task_id(base_id: str, next_due_date: date, pet: Pet) -> str:
        """Builds a unique recurring task ID by adding a date suffix and counter."""
        base = f"{base_id}-{next_due_date.strftime('%Y%m%d')}"
        existing_ids = {task.task_id for task in pet.tasks}
        candidate = base
        counter = 1
        while candidate in existing_ids:
            candidate = f"{base}-{counter}"
            counter += 1
        return candidate

    def organize_tasks(
        self,
        include_completed: bool = True,
        sort_by: str = "priority"
    ) -> List[Task]:
        """Returns a sorted list of tasks across pets."""
        tasks = self.get_all_tasks(include_completed=include_completed)
        if sort_by == "time":
            return sorted(
                tasks,
                key=lambda task: (
                    task.start_time_minutes if task.start_time_minutes is not None else 10**9,
                    -task.get_priority_value(),
                    task.duration_minutes,
                    task.title.lower(),
                )
            )
        if sort_by == "duration":
            return sorted(tasks, key=lambda task: task.duration_minutes)
        if sort_by == "frequency":
            return sorted(tasks, key=lambda task: task.frequency)
        if sort_by == "description":
            return sorted(tasks, key=lambda task: task.description.lower())
        return sorted(tasks, key=lambda task: task.get_priority_value(), reverse=True)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        status: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> List[Task]:
        """Filters tasks by pet name and completion status."""
        tasks = self.get_all_tasks(include_completed=True)
        if pet_name:
            tasks = [task for task in tasks if self._task_belongs_to_pet(task, pet_name)]
        if status:
            normalized = status.lower().strip()
            if normalized in {"completed", "done"}:
                tasks = [task for task in tasks if task.is_completed()]
            elif normalized in {"pending", "incomplete"}:
                tasks = [task for task in tasks if not task.is_completed()]
        if task_type:
            tasks = [task for task in tasks if task.task_type == task_type]
        return tasks

    def _task_belongs_to_pet(self, task: Task, pet_name: str) -> bool:
        """Returns True if the task appears in the specified pet's task list."""
        for pet in self.owner.pets:
            if pet.name == pet_name and task in pet.tasks:
                return True
        return False
