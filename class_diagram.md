# PawPal+ Class Diagram

This diagram shows the main classes for the PawPal+ pet care planning application.

```mermaid
classDiagram
    class UserInfo {
        -string name
        -int available_time_minutes
        -dict preferences
        +__init__(name, available_time_minutes, preferences)
        +get_available_time() int
        +set_preferences(preferences) void
        +get_name() string
    }

    class PetInfo {
        -string name
        -string species
        -int age
        -list~string~ special_needs
        +__init__(name, species, age, special_needs)
        +get_pet_info() dict
        +has_special_needs() bool
        +get_name() string
    }

    class Task {
        -string task_id
        -string title
        -int duration_minutes
        -string priority
        -string task_type
        -bool completed
        -string description
        -string frequency
        -int start_time_minutes
        -int recurrence_interval_days
        -date last_completed_date
        -list~string~ applicable_species
        -list~string~ preference_tags
        -list~string~ depends_on
        -bool requires_special_needs
        +__init__(task_id, title, duration_minutes, priority, task_type)
        +mark_completed() void
        +get_priority_value() int
        +is_completed() bool
        +is_due_on(target_date) bool
        +__str__() string
    }

    class Schedule {
        -datetime date
        -UserInfo owner
        -PetInfo pet
        -list~Task~ available_tasks
        -list~Task~ scheduled_tasks
        -int total_time_minutes
        -string explanation
        -list~Task~ conflicts
        +__init__(date, owner, pet, available_tasks)
        +generate_schedule() void
        +add_task_to_schedule(task) bool
        +validate_schedule() bool
        +get_explanation() string
        +calculate_total_time() int
        +get_scheduled_tasks() list~Task~
        +get_conflicts() list~Task~
    }

    class Pet {
        -string name
        -string species
        -int age
        -list~Task~ tasks
        +__init__(name, species, age)
        +add_task(task) void
        +remove_task(task_id) bool
        +get_tasks(include_completed) list~Task~
        +get_pending_tasks() list~Task~
    }

    class Owner {
        -string name
        -list~Pet~ pets
        +__init__(name)
        +add_pet(pet) void
        +remove_pet(pet_name) bool
        +get_pet(pet_name) Pet
        +get_all_tasks(include_completed) list~Task~
    }

    class Scheduler {
        -Owner owner
        +__init__(owner)
        +get_all_tasks(include_completed) list~Task~
        +get_tasks_by_pet(include_completed) dict
        +get_pending_tasks() list~Task~
        +detect_time_conflicts(include_completed) list~string~
        +organize_tasks(include_completed, sort_by) list~Task~
        +filter_tasks(pet_name, status, task_type) list~Task~
        +mark_task_completed(task_id) bool
    }

    Schedule *-- UserInfo : contains
    Schedule *-- PetInfo : contains
    Schedule o-- Task : uses
    Owner *-- Pet : owns
    Pet *-- Task : has
    Scheduler --> Owner : manages
    Scheduler o-- Task : organizes
    Task ..> PetInfo : applies to species
    Task ..> UserInfo : matches preferences
    Task ..> Task : depends on
```

## Class Descriptions

### UserInfo
Represents the pet owner with time constraints and preferences. Stores how much time the owner has available each day and their care preferences.

### PetInfo
Contains information about the pet including name, species (dog, cat, other), age, and any special needs that might affect care scheduling.

### Task
Represents individual pet care tasks such as walks, feeding, medications, grooming, and enrichment activities. Tasks include scheduling metadata like frequency, optional start times, and recurrence details.

### Schedule
Generates optimized daily pet care schedules for a specific owner and pet. It filters available tasks, handles conflicts, and explains scheduling decisions.

### Pet
Represents a specific pet and the list of tasks assigned to it.

### Owner
Represents the pet owner and manages their pets and combined task list.

### Scheduler
Provides cross-pet utilities like sorting, filtering, conflict detection, and completing recurring tasks.

## Relationships

- **Schedule → UserInfo** (Composition `*--`): Each schedule is created for a specific owner
- **Schedule → PetInfo** (Composition `*--`): Each schedule is created for a specific pet
- **Schedule → Task** (Aggregation `o--`): Schedule uses and organizes multiple Task objects
- **Owner → Pet** (Composition `*--`): Owner manages a collection of pets
- **Pet → Task** (Composition `*--`): Pet stores its assigned tasks
- **Scheduler → Owner** (Association `-->`): Scheduler operates on a specific owner
- **Scheduler → Task** (Aggregation `o--`): Scheduler sorts and filters tasks
- **Task → Task** (Dependency `..>`): Tasks can depend on other tasks
