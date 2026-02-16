from datetime import datetime

import streamlit as st
from pawpal_system import Owner, Pet, PetInfo, Schedule, Task, Scheduler, UserInfo

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input(
    "Available time (minutes)", min_value=0, max_value=600, value=120
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
if "user_info" not in st.session_state:
    st.session_state.user_info = UserInfo(
        name=owner_name, available_time_minutes=int(available_time)
    )
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)
if "task_counter" not in st.session_state:
    st.session_state.task_counter = 1

owner = st.session_state.owner
owner.name = owner_name
user_info = st.session_state.user_info
user_info.name = owner_name
user_info.available_time_minutes = int(available_time)
scheduler = st.session_state.scheduler
scheduler.owner = owner

if st.button("Add pet"):
    if owner.get_pet(pet_name):
        st.info("Pet already exists. Update its details below if needed.")
    else:
        owner.add_pet(Pet(name=pet_name, species=species))

pet = owner.get_pet(pet_name)
if pet:
    pet.species = species
else:
    st.info("Add a pet to start scheduling tasks.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
task_type = st.selectbox("Task type", ["walk", "feed", "play", "groom", "other"], index=0)

if st.button("Add task"):
    if not pet:
        st.warning("Add a pet before adding tasks.")
    else:
        task_id = f"TASK-{st.session_state.task_counter}"
        st.session_state.task_counter += 1
        pet.add_task(
            Task(
                task_id=task_id,
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                task_type=task_type,
            )
        )

pet_tasks = pet.get_tasks() if pet else []
if pet_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "id": task.task_id,
                "title": task.title,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "task_type": task.task_type,
                "completed": task.completed,
            }
            for task in pet_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not pet:
        st.warning("Add a pet before generating a schedule.")
    else:
        pet_info = PetInfo(name=pet.name, species=pet.species, age=pet.age)
        schedule = Schedule(
            date=datetime.now(),
            owner=user_info,
            pet=pet_info,
            available_tasks=pet.get_pending_tasks(),
        )
        schedule.generate_schedule()
        scheduled_tasks = schedule.get_scheduled_tasks()
        if scheduled_tasks:
            st.success("Schedule generated.")
            st.table(
                [
                    {
                        "id": task.task_id,
                        "title": task.title,
                        "duration_minutes": task.duration_minutes,
                        "priority": task.priority,
                        "task_type": task.task_type,
                    }
                    for task in scheduled_tasks
                ]
            )
        else:
            st.info("No tasks could be scheduled with the current constraints.")
        if schedule.get_explanation():
            st.markdown("### Explanation")
            st.text(schedule.get_explanation())