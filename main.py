"""
PawPal+ Demo Script
Demonstrates the pet care task scheduling system.
"""

from pawpal_system import Owner, Pet, Task

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
        description="Take Max for his morning walk around the neighborhood"
    )

    task2 = Task(
        task_id="task_002",
        title="Feed Breakfast",
        duration_minutes=10,
        priority="high",
        task_type="feeding",
        description="Give Max his breakfast (2 cups of dry food)"
    )

    task3 = Task(
        task_id="task_003",
        title="Brush Fur",
        duration_minutes=15,
        priority="medium",
        task_type="grooming",
        description="Brush Max's fur to prevent matting"
    )

    # Add tasks to dog
    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)

    # Create Tasks for Whiskers (the cat)
    task4 = Task(
        task_id="task_004",
        title="Feed Breakfast",
        duration_minutes=5,
        priority="high",
        task_type="feeding",
        description="Give Whiskers wet food for breakfast"
    )

    task5 = Task(
        task_id="task_005",
        title="Clean Litter Box",
        duration_minutes=10,
        priority="medium",
        task_type="cleaning",
        description="Scoop and clean Whiskers' litter box"
    )

    # Add tasks to cat
    cat.add_task(task4)
    cat.add_task(task5)

    # Print Today's Schedule
    print("=" * 60)
    print("TODAY'S SCHEDULE - PAWPAL+")
    print("=" * 60)
    print(f"Owner: {owner.name}")
    print(f"Pets: {len(owner.pets)}")
    print()

    # Display schedule for each pet
    for pet in owner.pets:
        print(f"\n{pet.name} ({pet.species.upper()}, Age: {pet.age})")
        print("-" * 60)

        tasks = pet.get_tasks(include_completed=False)

        if not tasks:
            print("  No tasks scheduled")
        else:
            # Sort tasks by priority (high to low)
            sorted_tasks = sorted(
                tasks,
                key=lambda t: t.get_priority_value(),
                reverse=True
            )

            total_time = 0
            for task in sorted_tasks:
                status = "✓" if task.completed else "○"
                print(f"  {status} [{task.priority.upper():6}] {task.title:20} ({task.duration_minutes} min)")
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
