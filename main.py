"""
PawPal+ Demo Script
Demonstrates the pet care task scheduling system.
"""

from pawpal_system import Owner, Pet, Scheduler, Task

def main():
    # Create an Owner
    owner = Owner(name="Sarah")

    # Create Pets
    dog = Pet(name="Max", species="dog", age=3)
    cat = Pet(name="Whiskers", species="cat", age=5)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create Tasks for Max (the dog)
    task1 = Task(
        task_id="task_001",
        title="Morning Walk",
        duration_minutes=30,
        priority="high",
        task_type="exercise",
        description="Take Max for his morning walk around the neighborhood",
        start_time_minutes=540,
        frequency="daily",
        last_completed_date=None,
    )

    task2 = Task(
        task_id="task_002",
        title="Feed Breakfast",
        duration_minutes=10,
        priority="high",
        task_type="feeding",
        description="Give Max his breakfast (2 cups of dry food)",
        start_time_minutes=480,
        frequency="daily",
        last_completed_date=None,
    )

    task3 = Task(
        task_id="task_003",
        title="Brush Fur",
        duration_minutes=15,
        priority="medium",
        task_type="grooming",
        description="Brush Max's fur to prevent matting",
        start_time_minutes=600,
        frequency="weekly",
        last_completed_date=None,
    )

    # Add tasks to dog in an out-of-order sequence
    dog.add_task(task3)
    dog.add_task(task1)
    dog.add_task(task2)

    # Create Tasks for Whiskers (the cat)
    task4 = Task(
        task_id="task_004",
        title="Feed Breakfast",
        duration_minutes=5,
        priority="high",
        task_type="feeding",
        description="Give Whiskers wet food for breakfast",
        start_time_minutes=480,
        frequency="daily",
        last_completed_date=None,
    )

    task5 = Task(
        task_id="task_005",
        title="Clean Litter Box",
        duration_minutes=10,
        priority="medium",
        task_type="cleaning",
        description="Scoop and clean Whiskers' litter box",
        start_time_minutes=550,
        frequency="daily",
        last_completed_date=None,
    )

    # Add tasks to cat in an out-of-order sequence
    cat.add_task(task5)
    cat.add_task(task4)

    # Print Today's Schedule
    print("=" * 60)
    print("TODAY'S SCHEDULE - PAWPAL+")
    print("=" * 60)
    print(f"Owner: {owner.name}")
    print(f"Pets: {len(owner.pets)}")
    print()

    scheduler = Scheduler(owner)
    sorted_by_time = scheduler.organize_tasks(include_completed=False, sort_by="time")

    print("ALL TASKS SORTED BY TIME")
    print("-" * 60)
    for task in sorted_by_time:
        time_label = (
            f"{task.start_time_minutes // 60:02d}:{task.start_time_minutes % 60:02d}"
            if task.start_time_minutes is not None
            else "--:--"
        )
        print(
            f"  {time_label} [{task.priority.upper():6}] {task.title:20} "
            f"({task.duration_minutes} min)"
        )
    print()

    print("FILTERED: ONLY PENDING DOG TASKS")
    print("-" * 60)
    pending_dog_tasks = scheduler.filter_tasks(pet_name="Max", status="pending")
    for task in pending_dog_tasks:
        print(f"  [{task.priority.upper():6}] {task.title:20} ({task.duration_minutes} min)")
    print()

    print("TIME CONFLICT WARNINGS")
    print("-" * 60)
    conflict_warnings = scheduler.detect_time_conflicts(include_completed=False)
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"  {warning}")
    else:
        print("  No time conflicts detected.")
    print()

    # Display schedule for each pet
    for pet in owner.pets:
        print(f"\n{pet.name} ({pet.species.upper()}, Age: {pet.age})")
        print("-" * 60)

        tasks = pet.get_tasks(include_completed=False)

        if not tasks:
            print("  No tasks scheduled")
        else:
            # Sort tasks by time for per-pet display
            sorted_tasks = sorted(
                tasks,
                key=lambda t: (
                    t.start_time_minutes if t.start_time_minutes is not None else 10**9,
                    -t.get_priority_value(),
                    t.duration_minutes,
                    t.title.lower(),
                )
            )

            total_time = 0
            for task in sorted_tasks:
                status = "✓" if task.completed else "○"
                time_label = (
                    f"{task.start_time_minutes // 60:02d}:{task.start_time_minutes % 60:02d}"
                    if task.start_time_minutes is not None
                    else "--:--"
                )
                print(
                    f"  {status} {time_label} [{task.priority.upper():6}] {task.title:20} "
                    f"({task.duration_minutes} min)"
                )
                print(f"      {task.description}")
                total_time += task.duration_minutes

            print(f"\n  Total time for {pet.name}: {total_time} minutes")

    # Summary
    print("\n" + "=" * 60)
    all_tasks = owner.get_all_tasks(include_completed=False)
    total_duration = sum(task.duration_minutes for task in all_tasks)
    print(f"SUMMARY: {len(all_tasks)} total tasks, {total_duration} minutes")
    print("=" * 60)

if __name__ == "__main__":
    main()
