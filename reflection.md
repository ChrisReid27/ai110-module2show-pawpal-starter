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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is time-first ordering vs priority ordering. It's reasonable because if a task has a fixed start time, scheduling it even when its priority is lower keeps the schedule realistic and prevents missed time-bound care.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
