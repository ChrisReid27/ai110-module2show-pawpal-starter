# PawPal+ Class Diagram

This diagram shows the four main classes for the PawPal+ pet care planning application.

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
        -list~string~ applicable_species
        -list~string~ preference_tags
        -list~string~ depends_on
        -bool requires_special_needs
        +__init__(task_id, title, duration_minutes, priority, task_type)
        +mark_completed() void
        +get_priority_value() int
        +is_completed() bool
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
        +__init__(date, owner, pet, available_tasks)
        +generate_schedule() void
        +add_task_to_schedule(task) bool
        +validate_schedule() bool
        +get_explanation() string
        +calculate_total_time() int
        +get_scheduled_tasks() list~Task~
    }

    Schedule *-- UserInfo : contains
    Schedule *-- PetInfo : contains
    Schedule o-- Task : uses
    Task ..> PetInfo : applies to species
    Task ..> UserInfo : matches preferences
```

## Class Descriptions

### UserInfo
Represents the pet owner with time constraints and preferences. Stores how much time the owner has available each day and their care preferences.

### PetInfo
Contains information about the pet including name, species (dog, cat, other), age, and any special needs that might affect care scheduling.

### Task
Represents individual pet care tasks such as walks, feeding, medications, grooming, and enrichment activities. Each task has a duration, priority level, and type.

### Schedule
The main orchestrator class that generates optimized daily pet care schedules. It considers the owner's available time, pet needs, and task priorities to create a feasible plan with explanations.

## Relationships

- **Schedule → UserInfo** (Composition `*--`): Each schedule is created for a specific owner
- **Schedule → PetInfo** (Composition `*--`): Each schedule is created for a specific pet
- **Schedule → Task** (Aggregation `o--`): Schedule uses and organizes multiple Task objects
