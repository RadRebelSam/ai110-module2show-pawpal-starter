"""Basic tests for PawPal core classes."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status() -> None:
    task = Task(description="Walk the dog", time_minutes=30, frequency="daily")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Milo", species="Dog")
    initial_count = len(pet.tasks)

    pet.add_task(Task(description="Feed breakfast", time_minutes=10, frequency="daily"))

    assert len(pet.tasks) == initial_count + 1


def test_sorting_by_time_of_day() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Milo", species="Dog")
    pet.add_task(Task(description="B task", time_minutes=10, time_of_day="09:00"))
    pet.add_task(Task(description="A task", time_minutes=10, time_of_day="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    tasks = scheduler.organize_tasks_by_time(include_completed=True)

    assert [task.description for task in tasks] == ["A task", "B task"]


def test_filtering_by_pet_and_status() -> None:
    owner = Owner(name="Alex")
    dog = Pet(name="Milo", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    dog.add_task(Task(description="Walk", time_minutes=30, completed=False))
    cat.add_task(Task(description="Feed", time_minutes=10, completed=True))
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    luna_completed = scheduler.filter_tasks(pet_name="Luna", status="completed")

    assert len(luna_completed) == 1
    assert luna_completed[0].description == "Feed"


def test_due_tasks_for_recurring_items() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Milo", species="Dog")
    pet.add_task(
        Task(
            description="Weekly grooming",
            time_minutes=25,
            frequency="weekly",
            last_completed_on=date.today() - timedelta(days=8),
        )
    )
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    due = scheduler.due_tasks(on_date=date.today())

    assert [task.description for task in due] == ["Weekly grooming"]


def test_detects_conflicting_tasks() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Milo", species="Dog")
    pet.add_task(Task(description="Task 1", time_minutes=30, time_of_day="08:00"))
    pet.add_task(Task(description="Task 2", time_minutes=15, time_of_day="08:20"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(include_completed=True)

    assert len(conflicts) == 1
    assert conflicts[0][0].description == "Task 1"
    assert conflicts[0][1].description == "Task 2"


def test_complete_daily_task_creates_new_pending_occurrence() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Milo", species="Dog")
    pet.add_task(
        Task(
            description="Morning walk",
            time_minutes=30,
            frequency="daily",
            time_of_day="07:30",
        )
    )
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    completed = scheduler.complete_task(pet_name="Milo", task_description="Morning walk")

    assert completed is True
    matching_tasks = [task for task in pet.tasks if task.description == "Morning walk"]
    assert len(matching_tasks) == 2
    assert any(task.completed for task in matching_tasks)
    assert any(not task.completed for task in matching_tasks)


def test_detect_time_conflict_warnings_for_duplicate_times() -> None:
    owner = Owner(name="Alex")
    dog = Pet(name="Milo", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    dog.add_task(Task(description="Walk", time_minutes=20, time_of_day="08:00"))
    cat.add_task(Task(description="Feed", time_minutes=10, time_of_day="08:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_time_conflict_warnings(include_completed=True)

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "multiple pets" in warnings[0]


def test_empty_pet_has_no_tasks_in_sorted_output() -> None:
    owner = Owner(name="Alex")
    owner.add_pet(Pet(name="Milo", species="Dog"))
    scheduler = Scheduler(owner)

    tasks = scheduler.organize_tasks_by_time(include_completed=False)
    warnings = scheduler.detect_time_conflict_warnings(include_completed=False)

    assert tasks == []
    assert warnings == []
