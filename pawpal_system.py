"""PawPal+ logic layer.

Core implementation for Task, Pet, Owner, and Scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple


@dataclass
class Task:
    """Represents a single care activity for a pet."""

    description: str
    time_minutes: int
    frequency: str = "daily"
    completed: bool = False
    time_of_day: str | None = None
    last_completed_on: date | None = None

    def mark_complete(self) -> None:
        self.completed = True
        self.last_completed_on = date.today()

    def mark_incomplete(self) -> None:
        self.completed = False

    def update_description(self, description: str) -> None:
        self.description = description

    def update_time(self, time_minutes: int) -> None:
        self.time_minutes = time_minutes

    def update_frequency(self, frequency: str) -> None:
        self.frequency = frequency

    def update_time_of_day(self, time_of_day: str | None) -> None:
        self.time_of_day = time_of_day

    def is_due(self, on_date: date | None = None) -> bool:
        """Return whether a recurring task should happen on a given day."""
        check_date = on_date or date.today()
        if self.last_completed_on is None:
            return True

        frequency_days = {"daily": 1, "weekly": 7, "monthly": 30}
        interval = frequency_days.get(self.frequency.lower(), 1)
        return check_date >= (self.last_completed_on + timedelta(days=interval))

    def create_next_occurrence(self) -> Task | None:
        """Create the next pending recurring task for daily/weekly frequencies."""
        if self.frequency.lower() not in {"daily", "weekly"}:
            return None
        return Task(
            description=self.description,
            time_minutes=self.time_minutes,
            frequency=self.frequency,
            completed=False,
            time_of_day=self.time_of_day,
            last_completed_on=None,
        )


@dataclass
class Pet:
    """Stores pet details and all of that pet's tasks."""

    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, description: str) -> bool:
        for index, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]

    def get_pending_tasks(self) -> List[Task]:
        return self.get_tasks(include_completed=False)


@dataclass
class Owner:
    """Manages multiple pets and provides task access across pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                del self.pets[index]
                return True
        return False

    def get_pet(self, pet_name: str) -> Pet | None:
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks

    def get_tasks_by_pet(self) -> Dict[str, List[Task]]:
        return {pet.name: pet.get_tasks() for pet in self.pets}

    def get_all_tasks_with_pet(
        self, include_completed: bool = True
    ) -> List[Tuple[str, Task]]:
        rows: List[Tuple[str, Task]] = []
        for pet in self.pets:
            for task in pet.get_tasks(include_completed=include_completed):
                rows.append((pet.name, task))
        return rows


class Scheduler:
    """The planning brain for organizing tasks across all pets."""

    _frequency_rank = {"daily": 0, "weekly": 1, "monthly": 2}

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def retrieve_all_tasks(self, include_completed: bool = False) -> List[Task]:
        return self.owner.get_all_tasks(include_completed=include_completed)

    def organize_tasks(self, include_completed: bool = False) -> List[Task]:
        tasks = self.retrieve_all_tasks(include_completed=include_completed)
        return sorted(
            tasks,
            key=lambda task: (
                self._frequency_rank.get(task.frequency.lower(), 99),
                task.time_minutes,
                task.description.lower(),
            ),
        )

    def organize_tasks_by_time(self, include_completed: bool = False) -> List[Task]:
        """Sort tasks by scheduled clock time, then by frequency and duration."""
        tasks = self.retrieve_all_tasks(include_completed=include_completed)
        return self.sort_by_time(tasks)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their HH:MM time value using a lambda key."""
        return sorted(
            tasks,
            key=lambda task: (
                task.time_of_day is None or self._parse_time_to_minutes(task.time_of_day) is None,
                self._parse_time_to_minutes(task.time_of_day) or 24 * 60,
                task.description.lower(),
            ),
        )

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Backward-compatible alias for sorting by time."""
        return self.sort_by_time(tasks)

    def filter_tasks(
        self,
        pet_name: str | None = None,
        status: str = "all",
        include_completed: bool = True,
    ) -> List[Task]:
        """Filter tasks by pet and completion status."""
        status_value = status.lower()
        task_rows = self.owner.get_all_tasks_with_pet(include_completed=include_completed)
        filtered: List[Task] = []

        for task_pet_name, task in task_rows:
            if pet_name and task_pet_name.lower() != pet_name.lower():
                continue
            if status_value == "completed" and not task.completed:
                continue
            if status_value == "pending" and task.completed:
                continue
            filtered.append(task)

        return filtered

    def filter_by(self, pet_name: str | None = None, completed: bool | None = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        task_rows = self.owner.get_all_tasks_with_pet(include_completed=True)
        filtered: List[Task] = []

        for task_pet_name, task in task_rows:
            if pet_name and task_pet_name.lower() != pet_name.lower():
                continue
            if completed is not None and task.completed != completed:
                continue
            filtered.append(task)

        return filtered

    def due_tasks(self, on_date: date | None = None, include_completed: bool = False) -> List[Task]:
        """Return tasks that are due on a specific date."""
        tasks = self.retrieve_all_tasks(include_completed=include_completed)
        return [task for task in tasks if task.is_due(on_date=on_date)]

    def detect_time_conflict_warnings(self, include_completed: bool = False) -> List[str]:
        """Return lightweight warning messages for tasks sharing the exact same HH:MM time."""
        buckets: Dict[str, List[Tuple[str, Task]]] = {}
        for pet_name, task in self.owner.get_all_tasks_with_pet(include_completed=include_completed):
            if task.time_of_day is None:
                continue
            if self._parse_time_to_minutes(task.time_of_day) is None:
                continue
            buckets.setdefault(task.time_of_day, []).append((pet_name, task))

        warnings: List[str] = []
        for time_value in sorted(buckets.keys()):
            entries = buckets[time_value]
            if len(entries) < 2:
                continue

            pet_names = sorted({pet_name for pet_name, _task in entries})
            if len(pet_names) == 1:
                scope = f"same pet ({pet_names[0]})"
            else:
                scope = f"multiple pets ({', '.join(pet_names)})"
            task_names = ", ".join(task.description for _pet_name, task in entries)
            warnings.append(f"{time_value}: {scope} have concurrent tasks -> {task_names}")

        return warnings

    def detect_conflicts(self, include_completed: bool = False) -> List[tuple[Task, Task]]:
        """Detect overlapping tasks using time_of_day and duration."""
        tasks = self.organize_tasks_by_time(include_completed=include_completed)
        conflicts: List[tuple[Task, Task]] = []
        time_tasks = [task for task in tasks if task.time_of_day is not None]

        for index in range(len(time_tasks) - 1):
            current = time_tasks[index]
            nxt = time_tasks[index + 1]
            current_start = self._parse_time_to_minutes(current.time_of_day)
            next_start = self._parse_time_to_minutes(nxt.time_of_day)
            if current_start is None or next_start is None:
                continue

            current_end = current_start + current.time_minutes
            if current_end > next_start:
                conflicts.append((current, nxt))

        return conflicts

    def get_tasks_by_frequency(self, frequency: str, include_completed: bool = False) -> List[Task]:
        target = frequency.lower()
        tasks = self.retrieve_all_tasks(include_completed=include_completed)
        return [task for task in tasks if task.frequency.lower() == target]

    def complete_task(self, pet_name: str, task_description: str) -> bool:
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return False

        for task in pet.tasks:
            if task.description == task_description:
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return True
        return False

    @staticmethod
    def _parse_time_to_minutes(time_value: str | None) -> int | None:
        if time_value is None:
            return None
        try:
            parsed = datetime.strptime(time_value, "%H:%M")
        except ValueError:
            return None
        return parsed.hour * 60 + parsed.minute


# Compatibility aliases for earlier UML naming.
CareTask = Task
PetOwner = Owner
