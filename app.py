import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
DATA_FILE = "data.json"

st.title("🐾 PawPal+")

# Streamlit reruns the script on each interaction, so keep long-lived
# objects in session_state and only create them once.
if "owner" not in st.session_state:
    st.session_state.owner = Owner.load_from_json(DATA_FILE)

st.markdown(
    """
Welcome to the PawPal+ starter app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name
st.session_state.owner.save_to_json(DATA_FILE)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
with col4:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"], index=0)
with col5:
    scheduled_time = st.text_input("Time (HH:MM)", value="08:00")

if st.button("Add task"):
    owner = st.session_state.owner
    pet = owner.get_pet(pet_name)
    if pet is None:
        pet = Pet(name=pet_name, species=species)
        owner.add_pet(pet)

    task = Task(
        description=task_title,
        time_minutes=int(duration),
        frequency=frequency,
        priority=priority,
        time_of_day=scheduled_time or None,
    )
    pet.add_task(task)
    owner.save_to_json(DATA_FILE)
    st.success(f"Added '{task_title}' for {pet.name}.")

all_tasks_rows = []
owner = st.session_state.owner
scheduler = Scheduler(owner)
for task_pet_name, task in owner.get_all_tasks_with_pet(include_completed=True):
    priority_emoji = {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}
    status_emoji = "✅ Done" if task.completed else "⏳ Pending"
    all_tasks_rows.append(
        {
            "pet": task_pet_name,
            "task": task.description,
            "time_of_day": task.time_of_day or "unscheduled",
            "duration_minutes": task.time_minutes,
            "priority": priority_emoji.get(task.priority.lower(), task.priority.title()),
            "frequency": task.frequency,
            "status": status_emoji,
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
    include_completed = selected_status in {"all", "completed"}
    pet_filter = None if selected_pet == "All pets" else selected_pet
    filtered_tasks = scheduler.filter_tasks(
        pet_name=pet_filter,
        status=selected_status,
        include_completed=include_completed,
    )
    schedule_tasks = scheduler.organize_tasks(include_completed=include_completed)
    if pet_filter is not None:
        schedule_tasks = [task for task in schedule_tasks if task in filtered_tasks]

    if not schedule_tasks:
        st.info("No tasks available to schedule yet.")
    else:
        st.markdown("### Today's Schedule")
        task_to_pet = {
            id(task): task_pet_name
            for task_pet_name, task in owner.get_all_tasks_with_pet(include_completed=True)
        }
        schedule_rows = [
            {
                "pet": task_to_pet.get(id(task), "Unknown"),
                "task": task.description,
                "time_of_day": task.time_of_day or "unscheduled",
                "duration_minutes": task.time_minutes,
                "priority": {"high": "🔴 High", "medium": "🟡 Medium", "low": "🟢 Low"}.get(
                    task.priority.lower(), task.priority.title()
                ),
                "frequency": task.frequency,
                "status": "✅ Done" if task.completed else "⏳ Pending",
            }
            for task in schedule_tasks
        ]
        st.table(schedule_rows)

        due_tasks = scheduler.sort_by_time([task for task in schedule_tasks if task.is_due()])
        due_count = len(due_tasks)
        st.caption(f"Due today: {due_count} task(s)")
        if due_tasks:
            st.success("Your due tasks are already sorted by time for quick planning.")

        warnings = scheduler.detect_time_conflict_warnings(include_completed=include_completed)
        if warnings:
            st.warning("Scheduling warning: two or more tasks share the same time.")
            for warning in warnings:
                st.write(f"- {warning}")
            st.info(
                "Suggestion: move one task by 10-30 minutes or complete one early "
                "to reduce stress for both pets and owner."
            )
        else:
            st.success("No same-time conflicts detected in this schedule.")

        suggestion = scheduler.next_available_slot(duration_minutes=30, include_completed=False)
        if suggestion:
            st.info(f"Next suggested 30-minute slot: {suggestion}")
