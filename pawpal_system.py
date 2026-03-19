"""PawPal+ logic layer.

Core implementation for Task, Pet, Owner, and Scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Task:
    """Represents a single care activity for a pet."""

    description: str
    time_minutes: int
    frequency: str = "daily"
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    def update_description(self, description: str) -> None:
        self.description = description

    def update_time(self, time_minutes: int) -> None:
        self.time_minutes = time_minutes

    def update_frequency(self, frequency: str) -> None:
        self.frequency = frequency


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
                return True
        return False


# Compatibility aliases for earlier UML naming.
CareTask = Task
PetOwner = Owner
