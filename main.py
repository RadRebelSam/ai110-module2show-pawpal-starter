"""Temporary terminal test script for PawPal+ logic."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(owner: Owner) -> None:
    scheduler = Scheduler(owner)
    tasks = scheduler.organize_tasks(include_completed=False)

    print("Today's Schedule")
    print("================")

    if not tasks:
        print("No tasks scheduled.")
        return

    for index, task in enumerate(tasks, start=1):
        print(
            f"{index}. {task.description} - {task.time_minutes} min "
            f"({task.frequency}, completed={task.completed})"
        )


def main() -> None:
    owner = Owner(name="Alex")

    dog = Pet(name="Milo", species="Dog", age=4)
    cat = Pet(name="Luna", species="Cat", age=2)

    dog.add_task(Task(description="Morning walk", time_minutes=30, frequency="daily"))
    dog.add_task(Task(description="Evening feeding", time_minutes=15, frequency="daily"))
    cat.add_task(Task(description="Grooming session", time_minutes=20, frequency="weekly"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    print_schedule(owner)


if __name__ == "__main__":
    main()
