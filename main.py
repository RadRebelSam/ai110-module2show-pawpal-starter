"""Temporary terminal test script for PawPal+ logic."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(owner: Owner) -> None:
    scheduler = Scheduler(owner)
    unsorted_tasks = scheduler.retrieve_all_tasks(include_completed=False)
    tasks = scheduler.sort_by_time(unsorted_tasks)

    print("Sorted Schedule (by HH:MM)")
    print("===========================")

    if not tasks:
        print("No tasks scheduled.")
        return

    for index, task in enumerate(tasks, start=1):
        print(
            f"{index}. {task.time_of_day or 'unscheduled'} - "
            f"{task.description} - {task.time_minutes} min "
            f"({task.frequency}, completed={task.completed})"
        )

    warnings = scheduler.detect_time_conflict_warnings(include_completed=False)
    if warnings:
        print("\nWarnings")
        print("========")
        for warning in warnings:
            print(f"- {warning}")


def main() -> None:
    owner = Owner(name="Alex")

    dog = Pet(name="Milo", species="Dog", age=4)
    cat = Pet(name="Luna", species="Cat", age=2)

    dog.add_task(
        Task(
            description="Evening feeding",
            time_minutes=15,
            frequency="daily",
            time_of_day="18:00",
        )
    )
    dog.add_task(
        Task(
            description="Morning walk",
            time_minutes=30,
            frequency="daily",
            time_of_day="07:30",
        )
    )
    cat.add_task(
        Task(
            description="Grooming session",
            time_minutes=20,
            frequency="weekly",
            time_of_day="07:30",
        )
    )
    cat.add_task(
        Task(
            description="Playtime",
            time_minutes=20,
            frequency="daily",
            time_of_day="19:00",
        )
    )
    cat.add_task(
        Task(
            description="Medication",
            time_minutes=20,
            frequency="daily",
            time_of_day="07:45",
            completed=True,
        )
    )

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    print("Pending tasks for Luna (filter_by pet + completed=False):")
    for task in scheduler.filter_by(pet_name="Luna", completed=False):
        print(f"- {task.description}")

    print("\nCompleted tasks (all pets):")
    for task in scheduler.filter_by(completed=True):
        print(f"- {task.description}")

    print("\nDue tasks today:")
    for task in scheduler.due_tasks():
        print(f"- {task.description}")

    scheduler.complete_task(pet_name="Milo", task_description="Morning walk")
    print("\nAfter completing Milo's daily walk, new pending occurrences:")
    for task in scheduler.filter_by(pet_name="Milo", completed=False):
        if task.description == "Morning walk":
            print(f"- {task.description} at {task.time_of_day} (completed={task.completed})")
    print()

    print_schedule(owner)


if __name__ == "__main__":
    main()
