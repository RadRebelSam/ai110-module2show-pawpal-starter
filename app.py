import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Streamlit reruns the script on each interaction, so keep long-lived
# objects in session_state and only create them once.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

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
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    scheduled_time = st.text_input("Time (HH:MM)", value="08:00")

if st.button("Add task"):
    owner = st.session_state.owner
    pet = owner.get_pet(pet_name)
    if pet is None:
        pet = Pet(name=pet_name, species=species)
        owner.add_pet(pet)

    # Map the UI priority input to the Task.frequency field in the current model.
    frequency_map = {"high": "daily", "medium": "weekly", "low": "monthly"}
    task = Task(
        description=task_title,
        time_minutes=int(duration),
        frequency=frequency_map.get(priority, "daily"),
        time_of_day=scheduled_time or None,
    )
    pet.add_task(task)
    st.success(f"Added '{task_title}' for {pet.name}.")

all_tasks_rows = []
for pet in st.session_state.owner.pets:
    for task in pet.tasks:
        all_tasks_rows.append(
            {
                "pet": pet.name,
                "task": task.description,
                "duration_minutes": task.time_minutes,
                "frequency": task.frequency,
                "completed": task.completed,
            }
        )

if all_tasks_rows:
    st.write("Current tasks:")
    st.table(all_tasks_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule from all tasks across your pets.")

all_pet_names = [pet.name for pet in st.session_state.owner.pets]
selected_pet = st.selectbox("Filter by pet", ["All pets", *all_pet_names])
selected_status = st.selectbox("Filter by status", ["all", "pending", "completed"], index=0)

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    include_completed = selected_status in {"all", "completed"}
    if selected_pet == "All pets":
        filtered_tasks = scheduler.filter_tasks(
            pet_name=None,
            status=selected_status,
            include_completed=include_completed,
        )
    else:
        filtered_tasks = scheduler.filter_tasks(
            pet_name=selected_pet,
            status=selected_status,
            include_completed=include_completed,
        )
    schedule_tasks = scheduler.sort_tasks_by_time(filtered_tasks)

    if not schedule_tasks:
        st.info("No tasks available to schedule yet.")
    else:
        st.markdown("### Today's Schedule")
        schedule_rows = []
        for task in schedule_tasks:
            pet_name_for_task = "Unknown"
            for pet in st.session_state.owner.pets:
                if task in pet.tasks:
                    pet_name_for_task = pet.name
                    break

            schedule_rows.append(
                {
                    "pet": pet_name_for_task,
                    "task": task.description,
                    "duration_minutes": task.time_minutes,
                    "frequency": task.frequency,
                    "time_of_day": task.time_of_day or "unscheduled",
                }
            )
        st.table(schedule_rows)

        due_count = len([task for task in schedule_tasks if task.is_due()])
        st.caption(f"Due today: {due_count} task(s)")

        conflicts = scheduler.detect_conflicts(include_completed=include_completed)
        if conflicts:
            st.warning("Possible conflicts detected:")
            for left, right in conflicts:
                st.write(
                    f"- {left.description} ({left.time_of_day}) overlaps with "
                    f"{right.description} ({right.time_of_day})"
                )
