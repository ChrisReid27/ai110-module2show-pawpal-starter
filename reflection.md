# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1st core action: User should be able to add information about their pets and also their own scehdule (their constraints).
2nd core action: Task management, which would be durations, reasoning, and the category of the task.
3rd core action: Generating and interacting with the schedule itself and being able to edit it the way they like.

Classes: Task management, pet info, user info, and generated schedule.
Task Management would contain name of task, duration, priority level, category (e.g., "Medical", "Exercise"), and if a task is mandatory.
Pet info would contain name, species, age, and a list of requirements list.
User info would contain ownership of pets, time windows, and limits/constraints.
Generated schedule would contain methods from data from the other classes to generate the schedule and provide explanation and allow for further manual edits.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design did change. One change I made was to avoid a logical bottleneck where there was no ordering or optimization policies defined. I had to change the schedule algorithm from being unspecified and defaulting to highest priority first. I made this change so the algorithm doesn't block shorter high priority needs when time could get tight and so it can manage special needs/changes from a user.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers time, priority, preferences, and frequencyies of tasks. The constraints that would be repeatedly necessary are the ones that would need to be included, the best example being times/durations of tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is time-first ordering vs priority ordering. It's reasonable because if a task has a fixed start time, scheduling it even when its priority is lower keeps the schedule realistic and prevents missed time-bound care.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used A.I. tools heavily, especially for debugging and for making my code present more organized. Questions that were very specific and targeted were the best. I did not utilize inline suggestions much, I would always ask questions that are similar in topic in batches to the main chat.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The chat suggested a change for pawpal_system that would have required changing my main.py and that would cause tests that previously passed in the suite to fail due to syntax. The code they suggested was more convoluted than the one they suggested so I stuck with my own. This was for def build_recurring_task_id.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Tests:
Verifies a task starts as incomplete and becomes completed after calling mark_completed().
Verifies adding a task to a pet increases the pet’s task count.
Verifies a pet with no tasks returns empty lists for all tasks and pending tasks.
Verifies a one-time task is not due after it has been completed.
Verifies a daily task becomes due one day after last completion.
Verifies a schedule with two tasks at the same start time orders by title and only schedules the first alphabetically.
Verifies the scheduler detects a time conflict when two pets have tasks with the same start time and reports the correct time.

These are important because they directly address the basic workflow for the app. These are the minimum tests that need to be in place for the bare bones app so that if I add more the basic app running is a non-issue.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I think my scheduler is ok but can use some polishing. An edge case I would add would be for task overlap not with start times but later on in task duration.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The UML diagram and the testing suite.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would try to make pawpal_system more readable and simple; improve human readability although it's not too bad right now.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The different modes (Ask, Plan, Agent) are all very useful at specific parts during development. The order for best results is in fact ask->plan->agent/edit or just plan then agent/edit.
