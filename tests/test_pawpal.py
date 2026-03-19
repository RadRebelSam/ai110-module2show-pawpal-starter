"""Basic tests for PawPal core classes."""

from pawpal_system import Pet, Task


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
